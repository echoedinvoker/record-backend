from typing import List, Union
from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import validates
from database import Base
import json

class Hope(Base):
    __tablename__ = 'hopes'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    name = Column(String)
    markdown_content = Column(String)
    parent_key = Column(String, nullable=True) 
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
    def task_order_list(self) -> List:
        if self.task_order is None:
            return []
        try:
            return json.loads(self.task_order) # type: ignore
        except json.JSONDecodeError:
            return []


    @task_order_list.setter
    def task_order_list(self, value):
        if value is None:
            self.task_order = None
        else:
            try:
                self.task_order = json.dumps(value)
            except (TypeError, ValueError):
                # Handle the error appropriately, maybe log it or raise a custom exception
                self.task_order = '[]'


class ColumnOrder(Base):
    __tablename__ = 'column_orders'
    id = Column(Integer, primary_key=True, index=True)
    column_order = Column(Text)

    @validates('column_order')
    def validate_column_ids(self, _, value: Union[List, str]) -> str:
        if isinstance(value, list):
            return json.dumps(value)
        return value

    @property
    def column_order_list(self) -> List:
        if isinstance(self.column_order, str):
            return json.loads(self.column_order) if self.column_order else []
        return []

    @column_order_list.setter
    def column_order_list(self, value):
        self.column_order = json.dumps(value)

class Precept(Base):
    __tablename__ = 'precepts'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    start_end_times = Column(String)
    base_multiplier = Column(Float, nullable=False)
    thresholds = Column(String)
    hope_key = Column(String, nullable=False)

