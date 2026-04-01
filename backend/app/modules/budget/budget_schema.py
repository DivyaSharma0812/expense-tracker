from marshmallow import Schema, fields, validate
from ..category.category_schema import CategorySchema


class BudgetSchema(Schema):
    id = fields.Int(dump_only=True)
    category_id = fields.Int(dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)
    year = fields.Int(dump_only=True)
    month = fields.Int(dump_only=True)
    amount = fields.Decimal(dump_only=True, as_string=True, places=2)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class BudgetCreateSchema(Schema):
    category_id = fields.Int(required=True)
    year = fields.Int(required=True, validate=validate.Range(min=2000, max=2100))
    month = fields.Int(required=True, validate=validate.Range(min=1, max=12))
    amount = fields.Decimal(required=True, places=2)


class BudgetUpdateSchema(Schema):
    amount = fields.Decimal(required=True, places=2)
