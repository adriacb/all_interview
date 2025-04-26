# CI/CD Setup Guide

## Overview

This guide explains how to set up Continuous Integration and Continuous Deployment (CI/CD) for the Sentiment Analysis Microservice using GitHub Actions.

## What is CI/CD?

CI/CD stands for Continuous Integration and Continuous Deployment. It's a way to automate the process of testing, building, and deploying your code.

### Continuous Integration (CI)
- Automatically runs tests when you push code
- Checks code style and quality
- Ensures your code works before it's merged

### Continuous Deployment (CD)
- Automatically builds your application
- Creates deployment packages
- Deploys to your server

## GitHub Actions Workflows

We'll create two main workflows:

### 1. Test and Lint Workflow
This workflow runs on every push and pull request to ensure code quality.

```yaml
name: Test and Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH
      - name: Install dependencies
        run: |
          uv sync
          uv pip install -e .
          uv pip install pytest pytest-cov flake8
      - name: Lint with flake8
        run: |
          flake8 src tests
      - name: Test with pytest
        run: |
          pytest --cov=src --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v1
```

### 2. Build and Deploy Workflow
This workflow runs when you want to release a new version.

```yaml
name: Build and Deploy

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t sentiment-analysis .
      - name: Push to Docker Hub
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: yourusername/sentiment-analysis:latest
```

## Setting Up the Workflows

1. Create a `.github/workflows` directory in your project
2. Create two files:
   - `test-and-lint.yml` for testing and linting
   - `build-and-deploy.yml` for building and deploying
3. Copy the workflow code into these files
4. Push to GitHub

## Required Secrets

You'll need to set up these secrets in your GitHub repository:

1. `DOCKERHUB_USERNAME`: Your Docker Hub username
2. `DOCKERHUB_TOKEN`: Your Docker Hub access token
3. `CODECOV_TOKEN`: Your Codecov token (for coverage reporting)

To add secrets:
1. Go to your GitHub repository
2. Click on "Settings"
3. Click on "Secrets and variables" > "Actions"
4. Click "New repository secret"
5. Add each secret with its value

## Monitoring Workflows

You can monitor your workflows:
1. Go to your GitHub repository
2. Click on "Actions"
3. You'll see all workflow runs and their status

## Troubleshooting

Common issues and solutions:

1. **Workflow fails to start**
   - Check if the workflow file is in the correct location
   - Verify the file has the correct extension (.yml)

2. **Tests failing**
   - Check the test logs for specific errors
   - Make sure all dependencies are installed

3. **Docker build failing**
   - Verify Dockerfile is correct
   - Check if Docker Hub credentials are valid

## Best Practices

1. **Keep workflows fast**
   - Only run necessary steps
   - Use caching where possible

2. **Secure your secrets**
   - Never hardcode secrets
   - Use GitHub's secret management

3. **Regular maintenance**
   - Update dependencies regularly
   - Review and update workflows as needed

## Next Steps

After setting up CI/CD:
1. Test the workflows by pushing code
2. Monitor the results
3. Adjust configurations as needed
4. Consider adding more advanced features like:
   - Automated version bumping
   - Staging deployments
   - Performance testing 