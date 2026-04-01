from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError
from ..category_schema import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from ..category_service import CategoryService
from ..types import CategoryCreateParams, CategoryUpdateParams
from ....application.errors import ValidationError

blueprint = Blueprint("categories", __name__)

_service = CategoryService()
_schema = CategorySchema()
_schema_many = CategorySchema(many=True)
_create_schema = CategoryCreateSchema()
_update_schema = CategoryUpdateSchema()


@blueprint.get("")
def list_categories():
    return jsonify({"data": _schema_many.dump(_service.get_all_categories())})


@blueprint.post("")
def create_category():
    try:
        data = _create_schema.load(request.get_json() or {})
    except MarshmallowValidationError as marshmallow_error:
        raise ValidationError("Invalid request data", details=marshmallow_error.messages)

    params = CategoryCreateParams(**data)
    category = _service.create_category(params)
    return jsonify({"data": _schema.dump(category)}), 201


@blueprint.get("/<int:category_id>")
def get_category(category_id: int):
    return jsonify({"data": _schema.dump(_service.get_category(category_id))})


@blueprint.put("/<int:category_id>")
def update_category(category_id: int):
    try:
        data = _update_schema.load(request.get_json() or {})
    except MarshmallowValidationError as marshmallow_error:
        raise ValidationError("Invalid request data", details=marshmallow_error.messages)

    if not data:
        raise ValidationError("No fields provided for update")

    params = CategoryUpdateParams(**data)
    category = _service.update_category(category_id, params)
    return jsonify({"data": _schema.dump(category)})


@blueprint.delete("/<int:category_id>")
def delete_category(category_id: int):
    _service.delete_category(category_id)
    return "", 204
