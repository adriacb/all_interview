# API Documentation

## Workflow
To analyze sentiment of comments, follow these steps:

1. First, get the list of available topics from the Feddit API:
```bash
GET http://localhost:8080/api/v1/subfeddits/
```

Response:
```json
[
  {
    "id": 1,
    "username": "user1",
    "title": "Dummy Topic 1",
    "description": "First dummy topic"
  },
  {
    "id": 2,
    "username": "user2",
    "title": "Dummy Topic 2",
    "description": "Second dummy topic"
  }
]
```

2. Then, analyze the sentiment of comments in a specific topic using our sentiment analysis API:
```bash
GET http://localhost:8000/api/v1/sentiment/{subfeddit}
```

For example, to analyze "Dummy Topic 2":
```bash
GET http://localhost:8000/api/v1/sentiment/Dummy%20Topic%202
```

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication.

## Endpoints

### 1. Get Sentiment Analysis for Subfeddit Comments

```
GET /api/v1/sentiment/{subfeddit}
```

Retrieves sentiment analysis for comments in a specific subfeddit.

#### Path Parameters
- `subfeddit` (required): The name of the subfeddit to analyze

#### Query Parameters
- `limit` (optional, integer): Number of comments to return (default: 25, min: 1, max: 100)
- `start_time` (optional, datetime): ISO 8601 datetime for filtering comments from this time
- `end_time` (optional, datetime): ISO 8601 datetime for filtering comments until this time
- `sort_by_score` (optional, boolean): Whether to sort results by sentiment score (default: false)

#### Response

##### Success Response (200 OK)
```json
{
  "analyses": [
    {
      "id": "string",
      "comment_id": "string",
      "comment_text": "string",
      "subfeddit_id": "string",
      "sentiment_score": float,
      "sentiment_label": "positive" | "negative" | "neutral",
      "created_at": "datetime"
    }
  ]
}
```

##### Error Responses

###### 400 Bad Request
```json
{
  "detail": "Invalid query parameters"
}
```

###### 404 Not Found
```json
{
  "detail": "Subfeddit not found"
}
```

###### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Examples

### Example 1: Get Recent Comments
```
GET /api/v1/sentiment/python?limit=10
```

Response:
```json
{
  "analyses": [
    {
      "id": "123",
      "comment_id": "456",
      "comment_text": "I love Python!",
      "subfeddit_id": "789",
      "sentiment_score": 0.8,
      "sentiment_label": "positive",
      "created_at": "2024-01-01T00:00:00"
    },
    {
      "id": "124",
      "comment_id": "457",
      "comment_text": "Python is difficult to learn.",
      "subfeddit_id": "789",
      "sentiment_score": -0.3,
      "sentiment_label": "negative",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### Example 2: Filter by Time Range
```bash
GET /api/v1/sentiment/Dummy%20Topic%202?start_time=2021-07-04T00:00:00Z&end_time=2021-07-06T10:00:02Z&sort_by_score=true
```

Response:
```json
{
  "analyses": [
    {
      "id": 33789,
      "comment_id": 33789,
      "comment_text": "Well done! Proud of you.",
      "subfeddit_id": 2,
      "sentiment_score": 0.9,
      "sentiment_label": "positive",
      "created_at": "2021-07-06T10:49:25"
    },
    {
      "id": 33731,
      "comment_id": 33731,
      "comment_text": "It looks great!",
      "subfeddit_id": 2,
      "sentiment_score": 0.8,
      "sentiment_label": "positive",
      "created_at": "2021-07-04T00:49:25"
    }
  ]
}
```

### Example 3: Sort by Polarity
```bash
GET /api/v1/sentiment/python?sort_by_score=true
```

## Rate Limiting
Currently, there are no rate limits implemented.

## Error Handling
The API uses standard HTTP status codes and returns error messages in a consistent format:

```json
{
  "detail": "Error message"
}
```

Common error scenarios:
- Invalid query parameters
- Subfeddit not found
- Internal server errors
- OpenAI API errors

## Pagination
The API supports pagination through the `limit` and `skip` parameters:
- `limit`: Controls how many items are returned in a single request
- `skip`: Controls how many items to skip from the beginning of the result set

## Notes
- The sentiment analysis is performed using OpenAI's GPT-4o mini
- Polarity scores range from -1.0 (most negative) to 1.0 (most positive)
- Classification is binary: "positive" or "negative"
- Comments are fetched from the Feddit API running on port 8080