from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    rating = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    role = Column(String(20), default="participant")  # 'participant' or 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user")
    task_assignment = relationship("TaskAssignment", back_populates="user", uselist=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)  # 'easy', 'medium', 'hard'
    points = Column(Integer, nullable=False)
    schema = Column(Text, nullable=False)  # DDL for creating tables
    tables = Column(JSON, nullable=False)  # Table structure with sample data
    expected_result = Column(JSON, nullable=False)  # Expected result for comparison
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="task")
    assignments = relationship("TaskAssignment", back_populates="task")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    query = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    points_earned = Column(Integer, default=0)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    task = relationship("Task", back_populates="submissions")


class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="task_assignment")
    task = relationship("Task", back_populates="assignments")


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    battle_start = Column(DateTime, nullable=True)
    round_duration_minutes = Column(Integer, default=120)
