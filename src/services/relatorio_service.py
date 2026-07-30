import os
from datetime import date, datetime
from fpdf import FPDF
from sqlalchemy import func
from src.database import db
from src.models.models import Pedido, ItemPedido, Produto


def _pedidos_do_dia(dia: date):
    inicio = datetime(dia.year, dia.month, dia.day, 0, 0, 0)
    fim = datetime(dia.year, dia.month, dia.day, 23, 59, 59)
    return Pedido.query.filter(Pedido.criado_em.between(inicio, fim)).all()


def _produtos_mais_vendidos(dia: date, limite=5):
    inicio = datetime(dia.year, dia.month, dia.day, 0, 0, 0)
    fim = datetime(dia.year, dia.month, dia.day, 23, 59, 59)

    resultado = (
        db.session.query(
            Produto.nome, func.sum(ItemPedido.quantidade).label("total")
        )
        .join(ItemPedido, ItemPedido.produto_id == Produto.id)
        .join(Pedido, Pedido.id == ItemPedido.pedido_id)
        .filter(Pedido.criado_em.between(inicio, fim))
        .group_by(Produto.nome)
        .order_by(func.sum(ItemPedido.quantidade).desc())
        .limit(limite)
        .all()
    )
    return resultado


def gerar_relatorio_diario(dia: date = None, pasta_saida="relatorios"):
    """Gera um PDF com o resumo de vendas do dia e retorna o caminho do arquivo."""
    dia = dia or date.today()
    pedidos = _pedidos_do_dia(dia)
    mais_vendidos = _produtos_mais_vendidos(dia)

    total_vendido = sum(float(p.valor_total) for p in pedidos)
    total_pedidos = len(pedidos)

    os.makedirs(pasta_saida, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_saida, f"relatorio_{dia.isoformat()}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Relatorio Diario de Vendas - {dia.strftime('%d/%m/%Y')}", ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.ln(4)
    pdf.cell(0, 8, f"Total de pedidos: {total_pedidos}", ln=True)
    pdf.cell(0, 8, f"Total vendido: R$ {total_vendido:.2f}", ln=True)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Produtos mais vendidos:", ln=True)
    pdf.set_font("Helvetica", "", 12)

    if mais_vendidos:
        for nome, total in mais_vendidos:
            pdf.cell(0, 8, f"- {nome}: {int(total)} unidades", ln=True)
    else:
        pdf.cell(0, 8, "Nenhum pedido registrado neste dia.", ln=True)

    pdf.output(caminho_arquivo)
    return caminho_arquivo
