from sqlalchemy import Column, Integer, String, Boolean

from .base import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    church = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    telegram_id = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(String, nullable=False)
    qr_code_path = Column(String, nullable=False)

    def __str__(self):
        return f'{self.name}'
