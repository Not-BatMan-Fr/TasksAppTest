import uuid
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel

# --- DATABASE CONFIGURATION ---
# Defines the location of our SQLite file
DATABASE_URL = "sqlite:///./tasks.db"
# The engine handles the actual communication with the DB file
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal is a factory for database connection objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class that our models will inherit from to be mapped to tables
Base = declarative_base()

# --- DATA MODELS ---
# This defines how the 'tasks' table looks in the database
class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True) # Unique ID for each task
    title = Column(String, nullable=False) # The name of the task
    status = Column(String, default="pending") # Task state

# This Pydantic model validates the data coming from the user/frontend
class TaskCreate(BaseModel):
    title: str

# Create the physical database file and tables based on the models above
Base.metadata.create_all(bind=engine)

# --- API INITIALIZATION ---
app = FastAPI()

# --- ENDPOINTS ---

# 1. READ: Get all tasks from the DB
@app.get("/tasks")
def get_tasks():
    db = SessionLocal() # Open a database connection
    tasks = db.query(Task).all() # Execute 'SELECT * FROM tasks'
    db.close() # Close connection to free up resources
    return tasks

# 2. CREATE: Add a new task to the DB
@app.post("/tasks")
def create_task(task_data: TaskCreate):
    db = SessionLocal() # Open connection
    # Create a new Task object with a unique ID
    new_task = Task(
        id=str(uuid.uuid4()), 
        title=task_data.title, 
        status="pending"
    )
    db.add(new_task) # Tell SQLAlchemy we want to save this object
    db.commit() # Save changes to the .db file
    db.refresh(new_task) # Get the latest data (like the generated ID)
    db.close() # Close connection
    return new_task