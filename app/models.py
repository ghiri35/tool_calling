from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from .db import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    has_escalated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.session_id"))
    user_id = Column(Integer, ForeignKey("users.id"))  # optional for anonymous
    sender = Column(String)  # "user", "bot", "assistant"
    message = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())



class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String, unique=True, index=True)  # UUID
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    ended_by = Column(String, nullable=True)  # user/bot/timeout
