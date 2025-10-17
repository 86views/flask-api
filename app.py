from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory data store
tasks = [
    {"id": 1, "title": "Sample Task", "completed": False, "created_at": datetime.now().isoformat()},
    {"id": 2, "title": "second Task", "completed": False, "created_at": datetime.now().isoformat()},
    {"id": 3, "title": "Third Task", "completed": True, "created_at": datetime.now().isoformat()},
    {"id": 4, "title": "Fourth Task", "completed": True, "created_at": datetime.now().isoformat()},
    {"id": 5, "title": "Fifth Task", "completed": True, "created_at": datetime.now().isoformat()},
]
task_counter = 2

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Tasks API",
        "endpoints": {
            "GET /tasks": "Get all tasks",
            "GET /tasks/<id>": "Get a specific task",
            "POST /tasks": "Create a new task",
            "PUT /tasks/<id>": "Update a task",
            "DELETE /tasks/<id>": "Delete a task"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks, "count": len(tasks)})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_counter
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": task_counter,
        "title": data['title'],
        "completed": data.get('completed', False),
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    task_counter += 1
    
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    if 'title' in data:
        task['title'] = data['title']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)