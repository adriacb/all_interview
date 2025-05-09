# Sentiment Analysis Microservice Architecture

## System Overview

```mermaid
graph TD
    Client[Client] -->|HTTP Request| SentimentAPI[Sentiment Analysis API]
    
    subgraph Sentiment Analysis Service
        SentimentAPI --> Service[Sentiment Service]
        Service --> FedditClient[Feddit Client]
        Service --> OpenAI[OpenAI GPT-4o mini]
        Service --> Repository[Analysis Repository]
    end
    
    FedditClient -->|HTTP Request| FedditAPI[Feddit API]
    FedditAPI -->|Subfeddit Data| FedditClient
    FedditAPI -->|Comments Data| FedditClient
    FedditClient -->|Data| Service
    Service -->|Comments| OpenAI
    OpenAI -->|Analysis Results| Service
    Service -->|Results| Repository
    Repository -->|Stored Data| Service
    Service -->|Response| SentimentAPI
    SentimentAPI -->|HTTP Response| Client
```

## Data Flow

```mermaid
sequenceDiagram
    participant Client
    participant SentimentAPI
    participant Service
    participant FedditClient
    participant FedditAPI
    participant OpenAI
    participant Repository
    
    Client->>SentimentAPI: GET /api/v1/sentiment/{subfeddit}
    SentimentAPI->>Service: Process Request
    
    Service->>FedditClient: Get Subfeddits
    FedditClient->>FedditAPI: GET /api/v1/subfeddits
    FedditAPI-->>FedditClient: Subfeddit Data
    FedditClient-->>Service: Subfeddit Details
    
    Service->>FedditClient: Get Comments
    FedditClient->>FedditAPI: GET /api/v1/comments?subfeddit_id={id}
    FedditAPI-->>FedditClient: Comments Data
    FedditClient-->>Service: Comments
    
    Service->>OpenAI: Analyze Sentiment
    OpenAI-->>Service: Analysis Results
    
    Service->>Repository: Store Results
    Repository-->>Service: Confirmation
    
    Service-->>SentimentAPI: Analysis Results
    SentimentAPI-->>Client: HTTP Response
```

## Component Architecture

```mermaid
graph TD
    subgraph API Layer
        Routes[API Routes]
        DTOs[Data Transfer Objects]
    end
    
    subgraph Application Layer
        Service[Sentiment Service]
        UseCases[Use Cases]
    end
    
    subgraph Domain Layer
        Entities[Domain Entities]
        Repositories[Repository Interfaces]
    end
    
    subgraph Infrastructure Layer
        FedditClient[Feddit API Client]
        OpenAI[OpenAI Integration]
        RepositoryImpl[Repository Implementation]
    end
    
    Routes --> DTOs
    DTOs --> Service
    Service --> UseCases
    UseCases --> Entities
    UseCases --> Repositories
    Repositories --> RepositoryImpl
    Service --> FedditClient
    Service --> OpenAI
```

## Key Components

1. **API Layer**
   - FastAPI application
   - REST endpoints
   - Request/Response DTOs

2. **Application Layer**
   - Sentiment Service
   - Use Cases
   - Business Logic

3. **Domain Layer**
   - Entities (Comment, SentimentAnalysis)
   - Repository Interfaces

4. **Infrastructure Layer**
   - Feddit API Client
   - OpenAI Integration
   - Repository Implementation

## Data Flow Steps

1. Client makes a request to analyze sentiment for a subfeddit
2. API routes receive the request and validate parameters
3. Sentiment Service orchestrates the analysis:
   - Fetches comments from Feddit API
   - Sends comments to OpenAI for analysis
   - Stores results in repository
4. Results are returned to the client

## Error Handling

```mermaid
graph TD
    Request[API Request] --> Validation{Input Validation}
    Validation -->|Valid| Processing[Process Request]
    Validation -->|Invalid| Error400[400 Bad Request]
    Processing --> FedditAPI[Feddit API Call]
    FedditAPI -->|Success| OpenAI[OpenAI Analysis]
    FedditAPI -->|Error| Error404[404 Not Found]
    OpenAI -->|Success| Response[Return Results]
    OpenAI -->|Error| Error500[500 Internal Error]
```

## Key Design Patterns

### 1. Dependency Injection
- Used for managing dependencies between components
- Implemented using FastAPI's dependency injection system
- Promotes loose coupling and testability

### 2. Repository Pattern
- Abstracts data access logic
- Provides a clean interface for data operations
- Enables easy switching of data sources

### 3. Factory Pattern
- Used for creating complex objects
- Implemented in the infrastructure layer for client creation

### 4. Strategy Pattern
- Used for sentiment analysis implementation
- Allows easy switching between different analysis strategies

## Error Handling

The system implements a comprehensive error handling strategy:

1. **Domain Errors**
   - Custom exceptions for domain-specific errors
   - Proper error categorization

2. **API Errors**
   - HTTP status codes
   - Consistent error response format
   - Detailed error messages

3. **Logging**
   - Structured logging
   - Different log levels
   - Error tracking

## Security Considerations

1. **API Security**
   - Input validation
   - Rate limiting (planned)
   - CORS configuration

2. **Data Security**
   - Environment variables for sensitive data
   - No sensitive data in logs
   - Secure API key handling

## Scalability

The architecture supports scalability through:

1. **Horizontal Scaling**
   - Stateless API design
   - Containerization support
   - Load balancing compatibility

2. **Performance Optimization**
   - Caching (planned)
   - Async operations
   - Efficient data processing

## Monitoring and Observability

1. **Logging**
   - Structured logging
   - Log levels
   - Error tracking

2. **Metrics**
   - API performance metrics
   - Error rates
   - Response times

## Future Considerations

1. **Planned Features**
   - Authentication and authorization
   - Rate limiting
   - Caching layer
   - More sophisticated sentiment analysis

2. **Architecture Evolution**
   - Microservices split (if needed)
   - Event-driven architecture
   - Message queue integration

## Service Dependencies

### Sentiment Analysis Service
The sentiment analysis service has the following dependencies:

1. **Feddit API**
   - Required for fetching subfeddits and comments
   - Configured via `FEDDIT_API_URL` environment variable
   - Must be available before the service starts

2. **OpenAI API**
   - Required for sentiment analysis
   - Configured via `OPENAI_API_KEY` environment variable
   - Must be available for sentiment analysis to work

3. **Memory Repository**
   - Used for storing sentiment analysis results
   - In-memory storage, no external database required
   - Data is not persisted between service restarts

### Docker Service Dependencies
In the Docker Compose configuration:
- `sentiment-analysis` service depends on `feddit` service
- No database dependency is required
- Services are connected via Docker's default network

### Health Checks
- Feddit API health check: `http://feddit:8080/api/v1/version`
- Sentiment Analysis health check: `http://localhost:8000/health`
- Health checks run every 30 seconds with 3 retries 

## Dependency Injection

The application uses FastAPI's built-in dependency injection system for managing dependencies. This approach provides several benefits:

1. **FastAPI Integration**
   - Native integration with FastAPI's dependency injection system
   - Automatic dependency resolution
   - Type-safe dependency injection
   - Easy testing through dependency overrides

2. **Dependency Providers**
   - Located in `src/sentiment_analysis/api/dependencies.py`
   - Each provider is a function that returns a dependency instance
   - Dependencies are lazily initialized
   - Easy to mock for testing

3. **Service Dependencies**
   ```python
   def get_sentiment_service(
       feddit_client: FedditClient = Depends(get_feddit_client),
       sentiment_analyzer: SentimentAnalyzer = Depends(get_sentiment_analyzer),
       sentiment_analysis_repository: SentimentAnalysisRepository = Depends(get_sentiment_analysis_repository)
   ) -> SentimentService:
       return SentimentService(
           feddit_client=feddit_client,
           sentiment_analyzer=sentiment_analyzer,
           sentiment_analysis_repository=sentiment_analysis_repository
       )
   ```

4. **Testing**
   - Dependencies can be easily overridden in tests
   - Each dependency can be mocked independently
   - Test fixtures can provide test-specific implementations 