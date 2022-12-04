from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String, default="active")
    state = Column(String, default="ack")
    retry_count = Column(String, default=0)
    filename = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __str__(self):
        return self.task_id


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    task_id = Column(String, ForeignKey("tasks.id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    task = relationship("Task")

    def __str__(self):
        return self.phone_number
