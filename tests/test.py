import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app, SessionLocal

# The TestClient allows us to make requests to our FastAPI app without running a server
client = TestClient(app)

# --- TEST 1: GET ALL TASKS (EMPTY) ---
def test_get_tasks_empty():
    # We use 'patch' to replace the real SessionLocal with a fake one
    with patch("main.SessionLocal") as mock_session:
        # Create a mock database object
        mock_db = MagicMock()
        # Tell the mock to return an empty list when .query().all() is called
        mock_db.query.return_value.all.return_value = []
        # Ensure our fake session is what the app uses
        mock_session.return_value = mock_db
        
        # Act: Make the request
        response = client.get("/tasks")
        
        # Assert: Check if the response is 200 OK and an empty list
        assert response.status_code == 200
        assert response.json() == []

# --- TEST 2: CREATE A TASK ---
def test_create_task():
    # We mock SessionLocal so we don't write a real file to disk
    with patch("main.SessionLocal") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        
        # Data we are sending to the API
        payload = {"title": "Learn Mocking"}
        
        # Act: Send a POST request
        response = client.post("/tasks", json=payload)
        
        # Assertions:
        # 1. Check if the status is 200 (Success)
        assert response.status_code == 200
        # 2. Verify the returned JSON contains our title
        assert response.json()["title"] == "Learn Mocking"
        # 3. Ensure the code actually tried to save to the DB
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()