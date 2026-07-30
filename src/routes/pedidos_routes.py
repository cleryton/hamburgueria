from flask import Blueprint, request, jsonify
from src.database import db
from src.models.models import Pedido, ItemPedido, Produto
from src.services.estoque_service import (
    verificar_disponibilidade,
    dar_baixa_estoque,
    EstoqueInsuficienteError,
)

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

STATUS_VALIDOS = ["recebido", "em_preparo", "pronto", "entregue", "cancelado"]


@pedidos_bp.post("")
def criar_pedido():
    """
    Corpo esperado:
    {
      "atendente_id": 1,
      "itens": [ {"produto_id": 1, "quantidade": 2}, ... ]
    }
    """
    dados = request.get_json()
    itens_dados = dados.get("itens", [])

    if not itens_dados:
        return jsonify({"erro": "O pedido precisa ter ao menos um item"}), 400

    pedido = Pedido(atendente_id=dados.get("atendente_id"), status="recebido")
    valor_total = 0

    for item in itens_dados:
        produto = Produto.query.get(item["produto_id"])
        if not produto or not produto.disponivel:
            return jsonify({"erro": f"Produto indisponivel: id {item['produto_id']}"}), 409

        disponivel, insumo_faltante = verificar_disponibilidade(produto)
        if not disponivel:
            return jsonify({
                "erro": "Estoque insuficiente para completar o pedido",
                "produto": produto.nome,
                "insumo_faltante": insumo_faltante,
            }), 409

        quantidade = item["quantidade"]
        preco_unitario = produto.preco
        valor_total += float(preco_unitario) * quantidade

        pedido.itens.append(ItemPedido(
            produto_id=produto.id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
        ))

    pedido.valor_total = valor_total
    db.session.add(pedido)
    db.session.commit()

    # Baixa de estoque após confirmar o pedido
    try:
        for item in pedido.itens:
            dar_baixa_estoque(item.produto, item.quantidade)
    except EstoqueInsuficienteError as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 409

    return jsonify({"id": pedido.id, "status": pedido.status, "valor_total": float(pedido.valor_total)}), 201


@pedidos_bp.get("")
def listar_pedidos():
    status_filtro = request.args.get("status")
    query = Pedido.query
    if status_filtro:
        query = query.filter_by(status=status_filtro)

    pedidos = query.order_by(Pedido.criado_em.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "status": p.status,
            "valor_total": float(p.valor_total),
            "criado_em": p.criado_em.isoformat(),
            "itens": [
                {"produto": i.produto.nome, "quantidade": i.quantidade}
                for i in p.itens
            ],
        }
        for p in pedidos
    ])


@pedidos_bp.get("/cozinha")
def fila_cozinha():
    """Pedidos pendentes de preparo, para o painel da cozinha."""
    pedidos = Pedido.query.filter(
        Pedido.status.in_(["recebido", "em_preparo"])
    ).order_by(Pedido.criado_em.asc()).all()

    return jsonify([
        {
            "id": p.id,
            "status": p.status,
            "itens": [
                {"produto": i.produto.nome, "quantidade": i.quantidade}
                for i in p.itens
            ],
        }
        for p in pedidos
    ])


@pedidos_bp.put("/<int:pedido_id>/status")
def atualizar_status(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    novo_status = request.get_json().get("status")

    if novo_status not in STATUS_VALIDOS:
        return jsonify({"erro": f"Status invalido. Use um de: {STATUS_VALIDOS}"}), 400

    pedido.status = novo_status
    db.session.commit()
    return jsonify({"id": pedido.id, "status": pedido.status})
