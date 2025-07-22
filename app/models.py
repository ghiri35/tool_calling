from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum
from .db import Base
from sqlalchemy.sql import func
import enum

class UserRole(enum.Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    has_escalated = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    status = Column(String, default="active")  # active, cancelled, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    dispatched_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String, nullable=False)  # e.g. "cancel_order"
    conditions = Column(String,nullable = False)
    on_deny_message = Column(String, nullable=True)
    escalate_after_retries = Column(Integer, default=2)  # how many times user can insist before escalation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


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
