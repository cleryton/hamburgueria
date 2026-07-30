from flask import Flask, jsonify
from src.config import Config
from src.database import db

from src.routes.produtos_routes import produtos_bp
from src.routes.insumos_routes import insumos_bp
from src.routes.pedidos_routes import pedidos_bp
from src.routes.relatorios_routes import relatorios_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(produtos_bp)
    app.register_blueprint(insumos_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(relatorios_bp)

    @app.get("/")
    def health_check():
        return jsonify({"status": "ok", "servico": "hamburgueria-api"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
