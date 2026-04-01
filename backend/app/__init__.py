import logging
from pathlib import Path
from flask import Flask, jsonify
from .config import config_map, DevelopmentConfig
from .extensions import database, marshmallow_extension, cors
from .application.errors import AppError
from .logging_config import configure_logging

logger = logging.getLogger(__name__)


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.instance_path = str(Path(__file__).resolve().parents[1] / "instance")
    Path(app.instance_path).mkdir(exist_ok=True)

    config_class = config_map.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)

    configure_logging(app.config.get("LOG_LEVEL", "INFO"))

    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "http://localhost:5173")}})
    database.init_app(app)
    marshmallow_extension.init_app(app)

    with app.app_context():
        from .modules.category.category_model import Category  # noqa: F401
        from .modules.expense.expense_model import Expense      # noqa: F401
        from .modules.budget.budget_model import Budget         # noqa: F401
        database.create_all()

    _register_blueprints(app)
    _register_error_handlers(app)

    logger.info("Application started", extra={"config": config_name})
    return app


def _register_blueprints(app: Flask) -> None:
    from .modules.category.rest_api.category_blueprint import blueprint as categories_bp
    from .modules.expense.rest_api.expense_blueprint import blueprint as expenses_bp
    from .modules.budget.rest_api.budget_blueprint import blueprint as budgets_bp
    from .modules.dashboard.rest_api.dashboard_blueprint import blueprint as dashboard_bp

    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(expenses_bp, url_prefix="/api/expenses")
    app.register_blueprint(budgets_bp, url_prefix="/api/budgets")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        if error.status_code >= 500:
            logger.exception("Server error: %s", error.message)
        else:
            logger.warning("Client error %s: %s", error.status_code, error.message)
        return error.to_response()

    @app.errorhandler(404)
    def handle_404(_error):
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Resource not found"}}), 404

    @app.errorhandler(405)
    def handle_405(_error):
        return jsonify({"error": {"code": "METHOD_NOT_ALLOWED", "message": "Method not allowed"}}), 405

    @app.errorhandler(Exception)
    def handle_unexpected(error: Exception):
        logger.exception("Unexpected error: %s", str(error))
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}}), 500
