# Setup Guide

## Prerequisites

- Python 3.8 or higher
- uv (Python package installer and virtual environment manager)
- OpenAI API key
- Access to Feddit API (running on port 8080)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sentiment-analysis
```

### 2. Create and Activate Virtual Environment

#### Windows
```bash
# Create virtual environment
uv venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

#### macOS/Linux
```bash
# Create virtual environment
uv venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install dependencies from pyproject.toml
uv sync
```

### 4. Environment Variables

Create a `.env` file in the root directory with the following content:

```env
OPENAI_API_KEY=your_api_key_here
FAST_API_PORT=8000
```

### 5. Verify Installation

Run the following command to verify the installation:

```bash
python -c "from sentiment_analysis import __version__; print(__version__)"
```

## Running the Service

### Development Mode

```bash
python -m sentiment_analysis.api.run
```

The API will be available at `http://localhost:8000`

### Production Mode

For production deployment, it's recommended to use a WSGI server like Gunicorn:

```bash
gunicorn sentiment_analysis.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## Configuration

The service can be configured through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `FAST_API_PORT` | Port for the FastAPI service | `8000` |

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_feddit_client.py

# Run with coverage
pytest --cov=sentiment_analysis tests/
```

### Test Categories

- Unit Tests: `tests/unit/`
- Integration Tests: `tests/integration/`
- API Tests: `tests/integration/api/`

## Troubleshooting

### Common Issues

1. **OpenAI API Key Not Found**
   - Ensure the `OPENAI_API_KEY` environment variable is set
   - Check that the `.env` file is in the correct location

2. **Feddit API Connection Issues**
   - Verify that the Feddit API is running using Docker
   - Check that the Docker container is up and running

3. **Import Errors**
   - Ensure the virtual environment is activated
   - Verify that all dependencies are installed using `uv sync`

### Logs

Logs are written to `logs/sentiment_analysis.log` by default. Check this file for detailed error messages.

## Development

### Code Style

This project follows PEP 8 style guidelines. Use the following tools:

```bash
# Run linter
flake8 src/ tests/

# Run type checking
mypy src/ tests/

# Format code
black src/ tests/
```

### Project Structure

```
sentiment-analysis/
├── src/
│   └── sentiment_analysis/
│       ├── api/              # FastAPI application
│       ├── application/      # Business logic
│       ├── domain/           # Domain models
│       └── infrastructure/   # External services
├── tests/                    # Test suite
├── docs/                     # Documentation
└── pyproject.toml           # Project configuration
```

## Updating Dependencies

To update dependencies:

1. Edit `pyproject.toml`
2. Run:
```bash
uv sync
```

## Uninstallation

To uninstall the package:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf .venv  # On Windows: rmdir /s /q .venv
``` 