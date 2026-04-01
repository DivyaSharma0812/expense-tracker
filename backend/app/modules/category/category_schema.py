from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    color = fields.Str(dump_only=True)
    icon = fields.Str(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    color = fields.Str(load_default="#6366f1", validate=validate.Length(equal=7))
    icon = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=10))


class CategoryUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))
    color = fields.Str(validate=validate.Length(equal=7))
    icon = fields.Str(allow_none=True, validate=validate.Length(max=10))
