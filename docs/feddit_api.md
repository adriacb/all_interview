# Feddit API Documentation

Feddit is a fake Reddit API that provides endpoints for accessing subfeddits and their comments. This documentation outlines the available endpoints and their response schemas.

## Base URL
```
http://0.0.0.0:8080
```

## Endpoints

### 1. Get All Subfeddits
Retrieves a list of all available subfeddits.

**Endpoint**: `GET /api/v1/subfeddits/`

**Query Parameters**:
- `limit` (optional): Number of subfeddits to return (default: 10)
- `skip` (optional): Number of subfeddits to skip (default: 0)

**Response Schema**:
```json
{
  "limit": 10,
  "skip": 0,
  "subfeddits": [
    {
      "id": 1,
      "username": "dummy_user",
      "title": "Pydantic Upgrading issue",
      "description": "I upgraded pydantic from v1 to v2, which brings a lot of problems."
    }
  ]
}
```

### 2. Get Subfeddit Details
Retrieves details of a specific subfeddit including its comments.

**Endpoint**: `GET /api/v1/subfeddit/`

**Query Parameters**:
- `limit` (optional): Number of comments to return (default: 10)
- `skip` (optional): Number of comments to skip (default: 0)

**Response Schema**:
```json
{
  "id": 1,
  "username": "dummy_user",
  "title": "Pydantic Upgrading issue",
  "description": "I upgraded pydantic from v1 to v2, which brings a lot of problems.",
  "limit": 10,
  "skip": 0,
  "comments": [
    {
      "id": 1,
      "username": "dummy_user",
      "text": "I upgraded pydantic from v1 to v2, which brings a lot of problems.",
      "created_at": 1695757477
    }
  ]
}
```

### 3. Get Comments
Retrieves comments for a specific subfeddit.

**Endpoint**: `GET /api/v1/comments/`

**Query Parameters**:
- `subfeddit_id` (required): ID of the subfeddit
- `limit` (optional): Number of comments to return (default: 10)
- `skip` (optional): Number of comments to skip (default: 0)

**Response Schema**:
```json
{
  "subfeddit_id": 1,
  "limit": 10,
  "skip": 0,
  "comments": [
    {
      "id": 1,
      "username": "dummy_user",
      "text": "I upgraded pydantic from v1 to v2, which brings a lot of problems.",
      "created_at": 1695757477
    }
  ]
}
```

## Data Types

### Comment
- `id`: Integer - Unique identifier of the comment
- `username`: String - User who made the comment
- `text`: String - Content of the comment
- `created_at`: Integer - Unix epoch timestamp of when the comment was created

### Subfeddit
- `id`: Integer - Unique identifier of the subfeddit
- `username`: String - User who created the subfeddit
- `title`: String - Title of the subfeddit
- `description`: String - Description of the subfeddit

## Pagination
All endpoints support pagination through the `limit` and `skip` parameters:
- `limit`: Controls how many items are returned in a single request
- `skip`: Controls how many items to skip from the beginning of the result set

## Notes
- There are 3 subfeddits available in total
- Each subfeddit contains more than 20,000 comments
- Use pagination parameters to handle large result sets efficiently 