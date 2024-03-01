from sqlalchemy.orm import DeclarativeBase, create_async_engine


engine = create_async_engine ()
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass
