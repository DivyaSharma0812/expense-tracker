from flask import jsonify


class AppError(Exception):
    """Base error class. All subclasses serialize to the standard error envelope."""

    status_code = 500
    error_code = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_response(self):
        body = {"error": {"code": self.error_code, "message": self.message}}
        if self.details:
            body["error"]["details"] = self.details
        return jsonify(body), self.status_code


class NotFoundError(AppError):
    status_code = 404
    error_code = "NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    error_code = "CONFLICT"


class ValidationError(AppError):
    status_code = 400
    error_code = "VALIDATION_ERROR"


class BusinessRuleError(AppError):
    """Passes schema validation but violates a domain rule."""

    status_code = 422
    error_code = "BUSINESS_RULE_VIOLATION"
