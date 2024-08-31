from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Column_, ColumnOrder, Task
from database import SessionLocal, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://44.201.114.25",
        "http://44.201.114.25:80",
        "http://172.31.95.142",
        "http://172.31.95.142:80",
        "http://localhost:5173",
        "http://app",
        "http://app:80",
        "http://localhost",
        "http://localhost:80",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TaskRequest(BaseModel):
    key: str
    name: str
    estimated_duration: int
    start_timestamp: Optional[int] = None
    consume_timestamp: Optional[int] = 0
    markdown_content: str = Field(max_length=200)
    ts: Optional[int] = None


class ColumnRequest(BaseModel):
    key: str
    task_order: str
    ts: Optional[int] = None

class ColumnOrderRequest(BaseModel):
    column_order: List[str]

@app.get("/tasks")
async def read_tasks(db: db_dependency):
    return db.query(Task).all()

@app.get("/tasks/key/{key}")
async def read_tasks_by_key(db: db_dependency, key: str):
    task = db.query(Task).filter(Task.key == key).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks/{task_id}")
async def read_task(db: db_dependency, task_id: int = Path(gt=0)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(db: db_dependency,
                      task_request: TaskRequest,
                      task_id: int = Path(gt=0)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.key = task_request.key
    task.name = task_request.name
    task.estimated_duration = task_request.estimated_duration
    task.start_timestamp = task_request.start_timestamp
    task.consume_timestamp = task_request.consume_timestamp
    task.markdown_content = task_request.markdown_content
    task.ts = task_request.ts
    db.add(task)
    db.commit()

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(db: db_dependency, task_request: TaskRequest):
    task = Task(**task_request.model_dump())
    db.add(task)
    db.commit()
    return {"id": task.id}


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(db: db_dependency, task_id: int = Path(gt=0)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()

@app.get("/columns")
async def read_columns(db: db_dependency):
    return db.query(Column_).all()

@app.get("/columns/key/{key}")
async def read_columns_by_key(db: db_dependency, key: str):
    column = db.query(Column_).filter(Column_.key == key).first()
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return column

@app.get("/columns/{column_id}")
async def read_column(db: db_dependency, column_id: int = Path(gt=0)):
    column = db.query(Column_).filter(Column_.id == column_id).first()
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return column
    
@app.post("/columns", status_code=status.HTTP_201_CREATED)
async def create_column(db: db_dependency, column_request: ColumnRequest):
    column = Column_(**column_request.model_dump())
    db.add(column)
    db.commit()

@app.put("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_column(db: db_dependency,
                        column_request: ColumnRequest,
                        column_id: int = Path(gt=0)):
    column = db.query(Column_).filter(Column_.id == column_id).first()
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    column.key = column_request.key
    column.task_order = column_request.task_order
    if column_request.ts is not None:
        column.ts = column_request.ts
    db.add(column)
    db.commit()

@app.get("/column_order")
async def get_column_order(db: db_dependency):
    column_order = db.query(ColumnOrder).first()
    if column_order is None:
        raise HTTPException(status_code=404, detail="Column order not found")
    return column_order.column_order_list

@app.post("/column_order", status_code=status.HTTP_201_CREATED)
async def build_column_order(db: db_dependency, column_order_request: ColumnOrderRequest):
    column_order = ColumnOrder(**column_order_request.model_dump())
    db.add(column_order)
    db.commit()

@app.put("/column_order", status_code=status.HTTP_204_NO_CONTENT)
async def update_column_order(db: db_dependency, column_order_request: ColumnOrderRequest):
    column_order = db.query(ColumnOrder).first()
    if column_order is None:
        raise HTTPException(status_code=404, detail="Column order not found")
    column_order.column_order_list = column_order_request.column_order
    db.add(column_order)
    db.commit()


