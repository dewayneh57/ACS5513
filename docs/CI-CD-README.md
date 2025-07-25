# CI/CD Pipeline Documentation

This repository includes a comprehensive Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub Actions.

## Pipeline Overview

The CI/CD pipeline automatically runs on every push to the `main` or `develop` branches and on pull requests to `main`. It consists of several jobs that ensure code quality and functionality.

## Pipeline Jobs

### 1. Backend Build (`backend-build`)
- **Purpose**: Build and test the backend web application
- **Steps**:
  - Checkout code
  - Set up Python 3.13 environment
  - Cache pip dependencies for faster builds
  - Install backend dependencies from `requirements.txt`
  - Create mock model files for testing
  - Run code linting with flake8
  - Test backend application startup
  - Test API endpoints (health check and prediction)

### 2. Frontend Build (`frontend-build`)
- **Purpose**: Build and test the frontend web application  
- **Steps**:
  - Checkout code
  - Set up Python 3.13 environment
  - Cache pip dependencies
  - Install frontend dependencies
  - Run code linting
  - Validate HTML templates
  - Test frontend application startup
  - Test frontend routes

### 3. Integration Tests (`integration-test`)
- **Purpose**: Test communication between frontend and backend
- **Dependencies**: Runs after both backend and frontend builds succeed
- **Steps**:
  - Install dependencies for both applications
  - Create mock models for testing
  - Framework ready for end-to-end testing expansion

### 4. Code Quality (`code-quality`)
- **Purpose**: Ensure code quality and security standards
- **Tools Used**:
  - **Black**: Code formatting checks
  - **isort**: Import sorting validation
  - **bandit**: Security vulnerability scanning
  - **safety**: Known vulnerability checks in dependencies

### 5. Build Summary (`build-summary`)
- **Purpose**: Provide overall build status summary
- **Dependencies**: Runs after all other jobs (regardless of success/failure)
- **Behavior**: Reports status of all pipeline components

## File Structure

```
.github/
  workflows/
    ci.yml              # Main CI/CD pipeline configuration

Back End Web App/
  requirements.txt      # Backend Python dependencies
  Dockerfile           # Backend container configuration
  tests/
    test_basic.py      # Basic backend tests

Front End Web App/
  requirements.txt      # Frontend Python dependencies  
  Dockerfile           # Frontend container configuration
  tests/
    test_basic.py      # Basic frontend tests

docker-compose.yml      # Multi-container deployment configuration
```

## Running Locally

### Prerequisites
- Python 3.13
- Git
- Docker (optional, for containerized deployment)

### Backend Testing
```bash
cd "Back End Web App"
pip install -r requirements.txt
python tests/test_basic.py
```

### Frontend Testing
```bash
cd "Front End Web App"
pip install -r requirements.txt
python tests/test_basic.py
```

### Full Application Deployment
```bash
# Using Docker Compose
docker-compose up --build

# Manual deployment (two terminals)
# Terminal 1 - Backend
cd "Back End Web App"
python -m flask run --port=10000

# Terminal 2 - Frontend  
cd "Front End Web App"
python -m flask run --port=5000
```

## Pipeline Features

### Caching
- Pip dependencies are cached to speed up builds
- Cache keys are based on requirements.txt file hashes

### Error Handling
- Each job includes comprehensive error handling
- Mock models are created when real models aren't available
- Graceful degradation for missing components

### Security
- Security scanning with bandit
- Dependency vulnerability checks with safety
- No hardcoded secrets or credentials

### Scalability
- Modular job structure allows easy expansion
- Parallel job execution where possible
- Environment-specific configurations

## Adding New Tests

### Backend Tests
Add new test functions to `Back End Web App/tests/test_basic.py` or create new test files:

```python
def test_new_feature():
    """Test description"""
    # Test implementation
    assert True
```

### Frontend Tests
Add new test functions to `Front End Web App/tests/test_basic.py`:

```python
def test_frontend_feature():
    """Test description"""
    # Test implementation
    assert True
```

## Pipeline Status

You can monitor pipeline status in several ways:

1. **GitHub Actions Tab**: View detailed logs and status
2. **README Badges**: Add status badges to display build status
3. **Email Notifications**: Configure in repository settings
4. **Slack/Teams Integration**: Set up webhook notifications

## Troubleshooting

### Common Issues

1. **Dependency Installation Failures**
   - Check `requirements.txt` files for version conflicts
   - Verify Python version compatibility

2. **Test Failures**
   - Review test logs in GitHub Actions
   - Run tests locally to reproduce issues

3. **Linting Errors**
   - Run `flake8` locally to identify issues
   - Follow PEP 8 style guidelines

4. **Security Scan Failures**
   - Update vulnerable dependencies
   - Review bandit security recommendations

### Local Debugging
```bash
# Run the same checks locally
pip install flake8 black isort safety bandit

# Code formatting
black --check "Back End Web App/app" "Front End Web App/app"

# Import sorting
isort --check-only "Back End Web App/app" "Front End Web App/app"

# Security scanning
bandit -r "Back End Web App/app" "Front End Web App/app"

# Dependency vulnerability check
safety check
```

## Future Enhancements

The pipeline is designed for easy expansion. Potential additions include:

- **Automated Deployment**: Deploy to staging/production on successful builds
- **Performance Testing**: Load testing and performance benchmarks
- **Code Coverage**: Track test coverage metrics
- **Notification Systems**: Slack, email, or Teams notifications
- **Multi-Environment Testing**: Test against different Python versions
- **Database Integration**: Test with real database connections
- **Documentation Generation**: Auto-generate API documentation

## Contributing

When contributing to this repository:

1. Ensure all tests pass locally before pushing
2. Follow the existing code style and linting rules
3. Add tests for new functionality
4. Update this documentation for significant changes

The CI/CD pipeline will automatically validate your changes and provide feedback on any issues.
