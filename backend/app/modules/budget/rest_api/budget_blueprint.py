from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError
from ..budget_schema import BudgetSchema, BudgetCreateSchema, BudgetUpdateSchema
from ..budget_service import BudgetService
from ..types import BudgetCreateParams, BudgetUpdateParams
from ....application.errors import ValidationError

blueprint = Blueprint("budgets", __name__)

_service = BudgetService()
_schema = BudgetSchema()
_schema_many = BudgetSchema(many=True)
_create_schema = BudgetCreateSchema()
_update_schema = BudgetUpdateSchema()


@blueprint.get("")
def list_budgets():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)
    category_id = request.args.get("category_id", type=int)
    budgets = _service.get_budgets(year=year, month=month, category_id=category_id)
    return jsonify({"data": _schema_many.dump(budgets)})


@blueprint.post("")
def create_budget():
    try:
        data = _create_schema.load(request.get_json() or {})
    except MarshmallowValidationError as marshmallow_error:
        raise ValidationError("Invalid request data", details=marshmallow_error.messages)

    params = BudgetCreateParams(**data)
    budget = _service.create_budget(params)
    return jsonify({"data": _schema.dump(budget)}), 201


@blueprint.get("/<int:budget_id>")
def get_budget(budget_id: int):
    return jsonify({"data": _schema.dump(_service.get_budget(budget_id))})


@blueprint.put("/<int:budget_id>")
def update_budget(budget_id: int):
    try:
        data = _update_schema.load(request.get_json() or {})
    except MarshmallowValidationError as marshmallow_error:
        raise ValidationError("Invalid request data", details=marshmallow_error.messages)

    params = BudgetUpdateParams(amount=data["amount"])
    budget = _service.update_budget(budget_id, params)
    return jsonify({"data": _schema.dump(budget)})


@blueprint.delete("/<int:budget_id>")
def delete_budget(budget_id: int):
    _service.delete_budget(budget_id)
    return "", 204
