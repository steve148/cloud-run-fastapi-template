"""SQLAlchemy base class for all models.

https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#using-a-declarative-base-class
"""
from sqlalchemy.orm import DeclarativeBase


# With SQLAlchemy 2, the DeclarativeBase class is no longer a singleton. This replaces
# the legacy form of using declarative_base() for generating the base class.
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#table-configuration-with-declarative
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    All SQLAlchemy models should inherit from this base.
    """

    __table_args__ = {"schema": "public", "extend_existing": True}
