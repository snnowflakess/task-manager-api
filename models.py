
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    text,
    func
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    role = Column(
        String(20),
        nullable=False,
        server_default=text("'USER'")
    )

    password_hash = Column(String(255), nullable=True)
    
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    tasks = relationship(
        "Task",
        back_populates="user",
        passive_deletes=True
    )

    comments = relationship(
        "Comment",
        back_populates="user",
        passive_deletes=True
    )


# TASK MODEL
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(
        String(20),
        nullable=False,
        server_default=text("'PENDING'")
    )

    priority = Column(
        String(20),
        nullable=False,
        server_default=text("'MEDIUM'")
    )

    due_date = Column(Date, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="tasks")

    comments = relationship(
        "Comment",
        back_populates="task",
        passive_deletes=True
    )


# COMMENT MODEL
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")
