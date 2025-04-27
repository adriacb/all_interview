# Sentiment Analysis Microservice for Feddit

A microservice that provides sentiment analysis for comments in Feddit (fake Reddit) subfeddits through a RESTful API.

## Features

- Sentiment analysis of Feddit comments using OpenAI's GPT-4o mini
- RESTful API endpoints for accessing sentiment analysis results
- Time range filtering for comments
- Sorting by polarity score
- Pagination support
- Comprehensive error handling

## Documentation

### Technical Documentation
- [Architecture Overview](docs/architecture.md) - System architecture and component interactions
- [API Documentation](http://localhost:8000/docs) - Swagger UI documentation
- [API Documentation (ReDoc)](http://localhost:8000/redoc) - Alternative API documentation
- [CI/CD Setup](docs/ci_cd_setup.md) - Continuous Integration and Deployment configuration
- [API Documentation](docs/api_documentation.md) - Detailed API specifications and examples
- [Feddit API](docs/feddit_api.md) - Documentation for the Feddit API integration

### Setup and Configuration
- [Setup Guide](docs/setup_guide.md) - Installation and configuration instructions

## Prerequisites

- Python 3.12
- OpenAI API key
- Access to Feddit API (running on port 8080)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sentiment-analysis
```

2. Create and activate a virtual environment:
```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv sync
```

4. Set up environment variables in .env file
```bash
# OpenAI settings
OPENAI_API_KEY=sk-proj-***

# App
FAST_API_PORT=8000
```

## Usage

1. Start the service:
```bash
uv run python -m sentiment_analysis.api.run
```

2. The API will be available at `http://localhost:8000`

## How to Use the API

### Prerequisites
- Make sure both the Feddit API and Sentiment Analysis service are running
- Feddit API should be available at `http://0.0.0.0:8080`
- Sentiment Analysis service should be available at `http://localhost:8000`

### Getting Started

1. **First, check available subfeddits**:
```bash
curl http://0.0.0.0:8080/api/v1/subfeddits/
```
This will show you the 3 available subfeddits and their titles.

2. **Analyze sentiment for a subfeddit**:
```bash
curl "http://localhost:8000/api/v1/sentiment/{subfeddit_title}?limit=25"
```
Replace `{subfeddit_title}` with the exact title of the subfeddit you want to analyze.

### Example Requests

1. **Basic sentiment analysis**:
```bash
curl "http://localhost:8000/api/v1/sentiment/Pydantic Upgrading issue?limit=25"
```

2. **With time range filtering**:
```bash
curl "http://localhost:8000/api/v1/sentiment/Pydantic Upgrading issue?limit=25&start_time=2024-01-01T00:00:00&end_time=2024-04-26T00:00:00"
```

3. **With sorting by polarity**:
```bash
curl "http://localhost:8000/api/v1/sentiment/Pydantic Upgrading issue?limit=25&sort_by=polarity"
```

### Response Example
```json
{
  "comments": [
    {
      "id": "string",
      "text": "string",
      "polarity_score": 0.8,
      "classification": "positive"
    }
  ],
  "metadata": {
    "limit": 25,
    "skip": 0,
    "total": 100
  }
}
```

### Using Docker

If you're using Docker, replace `localhost:8000` with the appropriate Docker container address (usually the same as localhost if using Docker's default networking).

## API Documentation

### Get Sentiment Analysis for Subfeddit Comments

```
GET /api/v1/sentiment/{subfeddit}
```

Retrieves sentiment analysis for the most recent comments in a subfeddit.

#### Query Parameters

- `limit` (optional): Number of comments to return (default: 25)
- `skip` (optional): Number of comments to skip (default: 0)
- `start_time` (optional): Unix timestamp for filtering comments from this time
- `end_time` (optional): Unix timestamp for filtering comments until this time
- `sort_by` (optional): Sort results by "polarity" (default: chronological)

#### Response

```json
{
  "comments": [
    {
      "id": "string",
      "text": "string",
      "polarity_score": float,
      "classification": "positive" | "negative"
    }
  ],
  "metadata": {
    "limit": 25,
    "skip": 0,
    "total": 100
  }
}
```

## Development

### Project Structure

```
sentiment-analysis/
├── src/
│   └── sentiment_analysis/
│       ├── api/              # FastAPI application
│       ├── application/      # Business logic
│       ├── domain/           # Domain models
│       └── infrastructure/   # External services and repositories
├── tests/                    # Test suite
└── docs/                     # Documentation
```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Use the following tools for code quality:

```bash
# Run linter
uv run flake8 src/ tests/
```

# Introduction
The `docker-compose.yml` file provides access to `Feddit` which is a fake reddit API built to complete the Allianz challenge. 

# How-to-run
1. Please make sure you have docker installed.
2. To run `Feddit` API locally in the terminal, replace `<path-to-docker-compose.yml>` by the actual path of the given `docker-compose.yml` file in `docker compose -f <path-to-docker-compose.yml> up -d`. It should be available in [http://0.0.0.0:8080](http://0.0.0.0:8080). 
3. To stop `Feddit` API in the terminal,  replace `<path-to-docker-compose.yml>` by the actual path of the given `docker-compose.yml` file in `docker compose -f <path-to-docker-compose.yml> down`.

# API Specification
Please visit either [http://0.0.0.0:8080/docs](http://0.0.0.0:8080/docs) or [http://0.0.0.0:8080/redoc](http://0.0.0.0:8080/redoc) for the documentation of available endpoints and examples of the responses.
There are 3 subfeddits available. For each subfeddit there are more than 20,000 comments, that is why we use pagination in the JSON response with the following parameters:

+ `skip` which is the number of comments to be skipped for each query
+ `limit` which is the max returned number of comments in a JSON response.

# Data Schemas
## Comment

+ **id**: unique identifier of the comment.
+ **username**: user who made/wrote the comment.
+ **text**: content of the comment in free text format.
+ **created_at**: timestamp in unix epoch time indicating when the comment was made/wrote.

## Subfeddit
+ **id**: unique identifier of the subfeddit
+ **username**: user who started the subfeddit.
+ **title**: topic of the subfeddit.
+ **description**: short description of the subfeddit.
+ **comments**: comments under the subfeddit.

