from marshmallow import Schema, fields, validate
from ..category.category_schema import CategorySchema


class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    category_id = fields.Int(dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)
    amount = fields.Decimal(dump_only=True, as_string=True, places=2)
    description = fields.Str(dump_only=True)
    date = fields.Date(dump_only=True)
    notes = fields.Str(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ExpenseCreateSchema(Schema):
    category_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, places=2)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    date = fields.Date(required=True)
    notes = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=2000))


class ExpenseUpdateSchema(Schema):
    category_id = fields.Int()
    amount = fields.Decimal(places=2)
    description = fields.Str(validate=validate.Length(min=1, max=500))
    date = fields.Date()
    notes = fields.Str(allow_none=True, validate=validate.Length(max=2000))
