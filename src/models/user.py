from sqlalchemy import Column, Integer, String, DateTime, func
from src.models.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    phone_number = Column(String)

    def __repr__(self):
        return f'<User id={self.id} email={self.email}/>'
