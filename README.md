# Flask REST API with CI/CD

A simple REST API built with Flask, containerized with Docker, and automated with GitHub Actions.

## Features

- RESTful API for task management
- Docker containerization
- Automated testing with pytest
- CI/CD pipeline with GitHub Actions
- Health check endpoint
- Automatic Docker Hub deployment

## API Endpoints

- `GET /` - API documentation
- `GET /health` - Health check
- `GET /tasks` - Get all tasks
- `GET /tasks/<id>` - Get specific task
- `POST /tasks` - Create new task
- `PUT /tasks/<id>` - Update task
- `DELETE /tasks/<id>` - Delete task

## Local Development

### Prerequisites

- Python 3.11+
- Docker and Docker Compose

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/flask-api.git
cd flask-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Run Tests
```bash
pytest test_app.py -v
```

## Docker Usage

### Build and run with Docker Compose:
```bash
docker-compose up -d
```

### Build manually:
```bash
docker build -t flask-api .
docker run -p 5000:5000 flask-api
```

## GitHub Actions Setup

### Required Secrets

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

1. `DOCKER_USERNAME` - Your Docker Hub username
2. `DOCKER_PASSWORD` - Your Docker Hub password or access token

### Workflow Triggers

- **Push to main/develop**: Runs tests and builds Docker image
- **Pull requests to main**: Runs tests only
- **Docker image push**: Only on push to main branch after successful tests

### Update Docker Image Name

In `.github/workflows/deploy.yml`, change:
```yaml
env:
  DOCKER_IMAGE: your-dockerhub-username/flask-api
```

To your actual Docker Hub username.

## Example Requests

### Create a task:
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "completed": false}'
```

### Get all tasks:
```bash
curl http://localhost:5000/tasks
```

### Update a task:
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "completed": true}'
```

### Delete a task:
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

## Project Structure
```
.
├── app.py                    # Main application
├── test_app.py              # Unit tests
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD pipeline
├── .gitignore
└── README.md
```

## CI/CD Pipeline

The GitHub Actions workflow:

1. **Test Job**: Runs on every push and pull request
   - Sets up Python environment
   - Installs dependencies
   - Runs pytest tests
   - Generates coverage report

2. **Build and Push Job**: Runs only on push to main after tests pass
   - Builds Docker image
   - Pushes to Docker Hub with tags
   - Uses layer caching for faster builds

## License

MIT License