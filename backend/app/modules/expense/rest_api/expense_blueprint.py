from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError
from ..expense_schema import ExpenseSchema, ExpenseCreateSchema, ExpenseUpdateSchema
from ..expense_service import ExpenseService
from ..types import ExpenseCreateParams, ExpenseUpdateParams
from ....application.errors import ValidationError

blueprint = Blueprint("expenses", __name__)

_service = ExpenseService()
_schema = ExpenseSchema()
_schema_many = ExpenseSchema(many=True)
_create_schema = ExpenseCreateSchema()
_update_schema = ExpenseUpdateSchema()


@blueprint.get("")
def list_expenses():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    category_id = request.args.get("category_id", type=int)
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    expenses, total = _service.get_expenses(
        page=page,
        per_page=per_page,
        category_id=category_id,
        year=year,
        month=month,
    )
    pages = (total + per_page - 1) // per_page if per_page else 1
    return jsonify({
        "data": _schema_many.dump(expenses),
        "meta": {"total": total, "page": page, "per_page": per_page, "pages": pages},
    })


@blueprint.post("")
def create_expense():
    try:
        data = _create_schema.load(request.get_json() or {})
    except MarshmallowValidationError as marshmallow_error:
        raise ValidationError("Invalid request data", details=marshmallow_error.messages)

    params = ExpenseCreateParams(
        category_id=data["category_id"],
        amount=data["amount"],
        description=data["description"],
        date=data["date"],
        notes=data.get("notes"),
    )
    expense, warnings = _service.create_expense(params)
    response = {"data": _schema.dump(expense)}
    if warnings:
        response["warnings"] = warnings
    return jsonify(response), 201


@blueprint.get("/<int:expense_id>")
def get_expense(expense_id: int):
    return jsonify({"data": _schema.dump(_service.get_expense(expense_id))})


@blueprint.put("/<int:expense_id>")
def update_expense(expense_id: int):
    try:
        data = _update_schema.load(request.get_json() or {})
    except MarshmallowValidationError as marshmallow_error:
        raise ValidationError("Invalid request data", details=marshmallow_error.messages)

    if not data:
        raise ValidationError("No fields provided for update")

    params = ExpenseUpdateParams(**data)
    expense, warnings = _service.update_expense(expense_id, params)
    response = {"data": _schema.dump(expense)}
    if warnings:
        response["warnings"] = warnings
    return jsonify(response)


@blueprint.delete("/<int:expense_id>")
def delete_expense(expense_id: int):
    _service.delete_expense(expense_id)
    return "", 204
