import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url ="http://test") as client: 
        response = await client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
            })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] == False

@pytest.mark.asyncio
async def test_get_tasks():
    async with AsyncClient(app=app, base_url ="http://test") as client: 
        response = await client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

