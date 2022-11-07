from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.models.database import Base


class Vote(Base):
    __tablename__ = 'votes'
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f'<Vote post_id={self.post_id} user_id={self.user_id}/>'
