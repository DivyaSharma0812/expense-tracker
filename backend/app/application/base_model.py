from datetime import datetime, timezone
from ..extensions import database


class BaseModel(database.Model):
    __abstract__ = True

    id = database.Column(database.Integer, primary_key=True)
    created_at = database.Column(
        database.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = database.Column(
        database.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
