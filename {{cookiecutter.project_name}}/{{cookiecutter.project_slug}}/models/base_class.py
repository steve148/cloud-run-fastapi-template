from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # Use UUID instead of int for primary key
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    # All records should have audit fields included which automatically get updated.
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
