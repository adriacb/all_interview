# Sentiment Analysis Microservice for Feddit

A microservice that provides sentiment analysis for comments in Feddit (fake Reddit) subfeddits through a RESTful API.

## Features

- Sentiment analysis of Feddit comments using OpenAI's GPT-4o mini
- RESTful API endpoints for accessing sentiment analysis results
- Time range filtering for comments
- Sorting by polarity score
- Pagination support
- Comprehensive error handling

## Prerequisites

- Python 3.8+
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
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
export OPENAI_API_KEY=your_api_key  # On Windows: set OPENAI_API_KEY=your_api_key
```

## Usage

1. Start the service:
```bash
python -m sentiment_analysis.api.run
```

2. The API will be available at `http://localhost:8000`

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
flake8 src/ tests/

# Run type checking
mypy src/ tests/
```

## License

[Your License Here]

## Contributing

[Your Contribution Guidelines Here]

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

