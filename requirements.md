# Sentiment Analysis Microservice for Feddit

## Project Overview
A microservice application that provides sentiment analysis for comments in Feddit (fake Reddit) subfeddits through a RESTful API.

## Core Requirements

### Main Functionality
1. Create a RESTful API endpoint that accepts a subfeddit name and returns:
   - List of 25 most recent comments
   - For each comment:
     - Unique identifier
     - Comment text
     - Polarity score
     - Classification (positive/negative)

### Optional Features
1. Time Range Filtering
   - Allow filtering comments by specific time range
2. Sorting Capability
   - Enable sorting results by polarity score
3. CI/CD Pipeline
   - Implement GitHub workflow for:
     - Linting checks
     - Running tests

## Technical Specifications

### Technology Stack
- Language: Python
- API Framework: FastAPI/Flask
- Sentiment Analysis: NLTK/TextBlob/VADER
- Testing: pytest
- Linting: flake8/black
- Container: Docker

### API Endpoints

#### Required Endpoint
```
GET /api/v1/sentiment/{subfeddit}
Response:
{
    "comments": [
        {
            "id": string,
            "text": string,
            "polarity_score": float,
            "classification": string  // "positive" or "negative"
        }
    ]
}
```

#### Optional Endpoints
```
GET /api/v1/sentiment/{subfeddit}?start_time={timestamp}&end_time={timestamp}
GET /api/v1/sentiment/{subfeddit}?sort_by=polarity
```

### Integration Requirements
- Connect to existing Feddit API (running on port 8080)
- Handle pagination for comment retrieval
- Process at least 25 comments per request

### Quality Requirements
1. Production-ready code
2. Clear documentation
3. Error handling
4. Unit tests
5. Code linting
6. English language for documentation

## Deliverables
1. Source code in a Git repository
2. Documentation:
   - Setup instructions
   - API documentation
   - Architecture overview
3. Tests
4. GitHub Actions workflow configuration 