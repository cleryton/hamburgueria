from datetime import datetime
from src.database import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    papel = db.Column(db.String(20), nullable=False)  # atendente, cozinha, gerente


class Insumo(db.Model):
    __tablename__ = "insumos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    unidade_medida = db.Column(db.String(20), nullable=False)  # un, kg, g, l, ml
    quantidade_estoque = db.Column(db.Float, nullable=False, default=0)
    estoque_minimo = db.Column(db.Float, nullable=False, default=0)

    @property
    def abaixo_do_minimo(self):
        return self.quantidade_estoque < self.estoque_minimo


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(60), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)

    insumos = db.relationship("ProdutoInsumo", backref="produto", cascade="all, delete-orphan")


class ProdutoInsumo(db.Model):
    """Ficha técnica: quanto de cada insumo um produto consome."""
    __tablename__ = "produto_insumo"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    insumo_id = db.Column(db.Integer, db.ForeignKey("insumos.id"), nullable=False)
    quantidade_utilizada = db.Column(db.Float, nullable=False)

    insumo = db.relationship("Insumo")


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    atendente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="recebido")
    # status possiveis: recebido, em_preparo, pronto, entregue, cancelado
    valor_total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemPedido", backref="pedido", cascade="all, delete-orphan")


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship("Produto")
