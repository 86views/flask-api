import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'endpoints' in data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tasks' in data
    assert 'count' in data

def test_create_task(client):
    new_task = {"title": "Test Task", "completed": False}
    response = client.post('/tasks', 
                          data=json.dumps(new_task),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'
    assert 'id' in data

def test_create_task_without_title(client):
    response = client.post('/tasks',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400

def test_get_single_task(client):
    response = client.get('/tasks/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 1

def test_get_nonexistent_task(client):
    response = client.get('/tasks/9999')
    assert response.status_code == 404

def test_update_task(client):
    update_data = {"title": "Updated Task", "completed": True}
    response = client.put('/tasks/1',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Task'
    assert data['completed'] == True

def test_delete_task(client):
    # First create a task
    new_task = {"title": "Task to Delete"}
    create_response = client.post('/tasks',
                                  data=json.dumps(new_task),
                                  content_type='application/json')
    task_id = json.loads(create_response.data)['id']
    
    # Then delete it
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404