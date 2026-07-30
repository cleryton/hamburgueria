from flask import Blueprint, jsonify
from src.services.relatorio_service import gerar_relatorio_diario
from src.services.email_service import enviar_relatorio_diario

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


@relatorios_bp.post("/diario")
def gerar_e_enviar_relatorio_diario():
    caminho_pdf = gerar_relatorio_diario()
    enviado = enviar_relatorio_diario(caminho_pdf)

    return jsonify({
        "arquivo_gerado": caminho_pdf,
        "email_enviado": enviado,
    })
