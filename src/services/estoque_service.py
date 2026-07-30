from src.database import db
from src.models.models import Insumo


class EstoqueInsuficienteError(Exception):
    def __init__(self, insumo_nome):
        self.insumo_nome = insumo_nome
        super().__init__(f"Estoque insuficiente para o insumo: {insumo_nome}")


def verificar_disponibilidade(produto):
    """Verifica se há estoque suficiente de cada insumo do produto."""
    for produto_insumo in produto.insumos:
        insumo = produto_insumo.insumo
        if insumo.quantidade_estoque < produto_insumo.quantidade_utilizada:
            return False, insumo.nome
    return True, None


def dar_baixa_estoque(produto, quantidade_pedida=1):
    """Desconta os insumos do estoque de acordo com a quantidade pedida."""
    for produto_insumo in produto.insumos:
        insumo = produto_insumo.insumo
        consumo_total = produto_insumo.quantidade_utilizada * quantidade_pedida

        if insumo.quantidade_estoque < consumo_total:
            raise EstoqueInsuficienteError(insumo.nome)

        insumo.quantidade_estoque -= consumo_total

    db.session.commit()


def listar_insumos_abaixo_do_minimo():
    insumos = Insumo.query.all()
    return [i for i in insumos if i.abaixo_do_minimo]
