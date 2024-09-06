from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import validates
from database import Base
import json

class Hope(Base):
    __tablename__ = 'hopes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    markdown_content = Column(String)
    parent_name = Column(String, nullable=True) 
    task_order = Column(Text)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    name = Column(String)
    estimated_duration = Column(Integer)
    start_timestamp = Column(Integer, nullable=True)
    ts = Column(Integer, nullable=True)
    consume_timestamp = Column(Integer)
    markdown_content = Column(String)
    parent_key = Column(Integer, nullable=True)


class Column_(Base):
    __tablename__ = 'columns'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    task_order = Column(Text)
    ts = Column(Integer, nullable=True)

    @validates('task_order')
    def validate_task_ids(self, _, value):
        if isinstance(value, list):
            return json.dumps(value)
        return value

    @property
    def task_order_list(self):
        return json.loads(self.task_order) if self.task_order else []

    @task_order_list.setter
    def task_order_list(self, value):
        self.task_order = json.dumps(value)


class ColumnOrder(Base):
    __tablename__ = 'column_orders'
    id = Column(Integer, primary_key=True, index=True)
    column_order = Column(Text)

    @validates('column_order')
    def validate_column_ids(self, _, value):
        if isinstance(value, list):
            return json.dumps(value)
        return value

    @property
    def column_order_list(self):
        return json.loads(self.column_order) if self.column_order else []

    @column_order_list.setter
    def column_order_list(self, value):
        self.column_order = json.dumps(value)
