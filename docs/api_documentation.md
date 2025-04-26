# API Documentation

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
- `limit` (optional, integer): Number of comments to return (default: 25, max: 100)
- `skip` (optional, integer): Number of comments to skip (default: 0)
- `start_time` (optional, integer): Unix timestamp for filtering comments from this time
- `end_time` (optional, integer): Unix timestamp for filtering comments until this time
- `sort_by` (optional, string): Sort results by "polarity" (default: chronological)

#### Response

##### Success Response (200 OK)
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
  "comments": [
    {
      "id": "123",
      "text": "I love Python!",
      "polarity_score": 0.8,
      "classification": "positive"
    },
    {
      "id": "124",
      "text": "Python is difficult to learn.",
      "polarity_score": -0.3,
      "classification": "negative"
    }
  ],
  "metadata": {
    "limit": 10,
    "skip": 0,
    "total": 1000
  }
}
```

### Example 2: Filter by Time Range
```
GET /api/v1/sentiment/python?start_time=1609459200&end_time=1612137600
```

### Example 3: Sort by Polarity
```
GET /api/v1/sentiment/python?sort_by=polarity
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