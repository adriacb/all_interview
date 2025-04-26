# Use Python 3.12 slim image
FROM python:3.12-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONPATH=/app

# Copy the project into the image
COPY . /app

# Set working directory
WORKDIR /app

# Install dependencies using uv
RUN uv venv .venv
RUN uv sync 
RUN uv pip install -e .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with environment variables
CMD ["uv", "run", "uvicorn", "sentiment_analysis.api.run:app", "--host", "0.0.0.0", "--port", "8000"]