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
  - Test Gunicorn deployment compatibility

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
  - Test Gunicorn deployment compatibility

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
    deploy.yml          # Heroku deployment pipeline

Back End Web App/
  requirements.txt      # Backend Python dependencies
  Procfile             # Heroku deployment configuration
  runtime.txt          # Python version specification
  tests/
    test_basic.py      # Basic backend tests

Front End Web App/
  requirements.txt      # Frontend Python dependencies
  Procfile             # Heroku deployment configuration
  runtime.txt          # Python version specification
  tests/
    test_basic.py      # Basic frontend tests
```

## Running Locally

### Prerequisites

- Python 3.13
- Git
- Heroku CLI (for manual deployment)

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

### Local Gunicorn Testing

```bash
# Test Backend with Gunicorn
cd "Back End Web App"
gunicorn --bind 0.0.0.0:10000 app:app

# Test Frontend with Gunicorn
cd "Front End Web App"
gunicorn --bind 0.0.0.0:5000 app:app
```

### Full Application Deployment

````bash
# Manual deployment (two terminals)
# Terminal 1 - Backend
cd "Back End Web App"
gunicorn --bind 0.0.0.0:10000 app:app

# Terminal 2 - Frontend
cd "Front End Web App"
gunicorn --bind 0.0.0.0:5000 app:app
```## Pipeline Features

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
````

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

- **Automated Deployment**: Deploy to staging/production on successful builds ✅ (Heroku deployment included)
- **Performance Testing**: Load testing and performance benchmarks
- **Code Coverage**: Track test coverage metrics
- **Notification Systems**: Slack, email, or Teams notifications
- **Multi-Environment Testing**: Test against different Python versions
- **Database Integration**: Test with real database connections
- **Documentation Generation**: Auto-generate API documentation

## Heroku Deployment

### Setup Required Secrets

To enable automatic Heroku deployment, add these secrets to your GitHub repository:

1. Go to your repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `HEROKU_API_KEY`: Your Heroku API key (found in Account Settings)
   - `HEROKU_EMAIL`: Your Heroku account email
   - `HEROKU_BACKEND_APP_NAME`: Name of your backend Heroku app
   - `HEROKU_FRONTEND_APP_NAME`: Name of your frontend Heroku app

### Manual Heroku Deployment

```bash
# Install Heroku CLI
# Create Heroku apps
heroku create your-backend-app-name
heroku create your-frontend-app-name

# Deploy Backend
cd "Back End Web App"
git init
heroku git:remote -a your-backend-app-name
git add .
git commit -m "Initial backend deployment"
git push heroku main

# Deploy Frontend
cd "../Front End Web App"
git init
heroku git:remote -a your-frontend-app-name
git add .
git commit -m "Initial frontend deployment"
git push heroku main
```

### Heroku Configuration

Each application includes:

- **Procfile**: Defines how Heroku runs your application using Gunicorn
- **runtime.txt**: Specifies Python version (3.13.5)
- **requirements.txt**: Lists all dependencies including Gunicorn

The deployment pipeline automatically:

1. Runs all CI tests
2. Deploys backend first (dependency for frontend)
3. Deploys frontend
4. Provides deployment URLs and status

## Contributing

When contributing to this repository:

1. Ensure all tests pass locally before pushing
2. Follow the existing code style and linting rules
3. Add tests for new functionality
4. Update this documentation for significant changes

The CI/CD pipeline will automatically validate your changes and provide feedback on any issues.
