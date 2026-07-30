from flask import Blueprint, request, jsonify
from src.database import db
from src.models.models import Insumo
from src.services.estoque_service import listar_insumos_abaixo_do_minimo
from src.services.email_service import notificar_estoque_baixo

insumos_bp = Blueprint("insumos", __name__, url_prefix="/insumos")


@insumos_bp.get("")
def listar_insumos():
    insumos = Insumo.query.all()
    return jsonify([
        {
            "id": i.id,
            "nome": i.nome,
            "unidade_medida": i.unidade_medida,
            "quantidade_estoque": i.quantidade_estoque,
            "estoque_minimo": i.estoque_minimo,
            "abaixo_do_minimo": i.abaixo_do_minimo,
        }
        for i in insumos
    ])


@insumos_bp.post("")
def criar_insumo():
    dados = request.get_json()
    insumo = Insumo(
        nome=dados["nome"],
        unidade_medida=dados["unidade_medida"],
        quantidade_estoque=dados.get("quantidade_estoque", 0),
        estoque_minimo=dados.get("estoque_minimo", 0),
    )
    db.session.add(insumo)
    db.session.commit()
    return jsonify({"id": insumo.id}), 201


@insumos_bp.get("/alertas")
def listar_alertas_estoque():
    criticos = listar_insumos_abaixo_do_minimo()
    return jsonify([{"id": i.id, "nome": i.nome, "quantidade_estoque": i.quantidade_estoque} for i in criticos])


@insumos_bp.post("/alertas/notificar")
def notificar_alertas_estoque():
    criticos = listar_insumos_abaixo_do_minimo()
    enviado = notificar_estoque_baixo(criticos)
    return jsonify({"notificacao_enviada": enviado, "quantidade_criticos": len(criticos)})
