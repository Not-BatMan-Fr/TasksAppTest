import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db

# 1. SETUP: Create a separate database file just for testing
TEST_DATABASE_URL = "sqlite:///./test_tasks.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. FIXTURE: This runs before and after your tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)
    yield # This is where the actual tests run
    # TEARDOWN: Delete the test file after all tests finish
    if os.path.exists("./test_tasks.db"):
        os.remove("./test_tasks.db")

# 3. OVERRIDE: Tell FastAPI to use our test DB instead of the real one
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- THE ACTUAL TESTS ---

def test_create_and_read_task():
    # Step A: Create a task
    create_resp = client.post("/tasks", json={"title": "Test Real DB"})
    assert create_resp.status_code == 200
    
    # Step B: Read it back to ensure it was actually saved
    read_resp = client.get("/tasks")
    data = read_resp.json()
    
    assert len(data) > 0
    assert data[0]["title"] == "Test Real DB"