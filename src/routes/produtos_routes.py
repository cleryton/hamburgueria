from flask import Blueprint, request, jsonify
from src.database import db
from src.models.models import Produto

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")


@produtos_bp.get("")
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "categoria": p.categoria,
            "preco": float(p.preco),
            "disponivel": p.disponivel,
        }
        for p in produtos
    ])


@produtos_bp.post("")
def criar_produto():
    dados = request.get_json()
    produto = Produto(
        nome=dados["nome"],
        categoria=dados["categoria"],
        preco=dados["preco"],
        disponivel=dados.get("disponivel", True),
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify({"id": produto.id}), 201


@produtos_bp.put("/<int:produto_id>")
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    dados = request.get_json()

    produto.nome = dados.get("nome", produto.nome)
    produto.categoria = dados.get("categoria", produto.categoria)
    produto.preco = dados.get("preco", produto.preco)
    produto.disponivel = dados.get("disponivel", produto.disponivel)

    db.session.commit()
    return jsonify({"mensagem": "Produto atualizado"})


@produtos_bp.delete("/<int:produto_id>")
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto excluido"})
