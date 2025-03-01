from datetime import datetime, timezone
from sqlalchemy import DateTime, Column
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    """FastAPI mixins which automatically add TIMESTAMP column to your model"""

    created = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )
    modified = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )
