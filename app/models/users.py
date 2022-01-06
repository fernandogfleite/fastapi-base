from app.db import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(255), index=True)
    password = Column(String(255), index=True)
    is_active = Column(Boolean, default=True, index=True)
