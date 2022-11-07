from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.models.database import Base

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Todo id={self.id} description={self.description} completed={self.completed}/>'
