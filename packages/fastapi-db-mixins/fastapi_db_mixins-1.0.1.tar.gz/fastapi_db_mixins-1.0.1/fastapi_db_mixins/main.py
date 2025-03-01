from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    """FastAPI mixins which automatically add TIMESTAMP column to your model"""

    created = Column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False
    )
    modified = Column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )
