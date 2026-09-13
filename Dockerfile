# Base image: official Python, slim variant to keep image size down
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install uv (the same tool you've used locally all week)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first (before the rest of the code)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies (this layer gets cached if pyproject.toml/uv.lock don't change)
RUN uv sync --frozen --no-dev

# Copy the rest of the project
COPY src/ ./src/
COPY api/ ./api/
COPY artifacts/ ./artifacts/
COPY data/raw/store.csv ./data/raw/store.csv
COPY data/raw/train.csv ./data/raw/train.csv

# Expose the port uvicorn will run on
EXPOSE 8000

# Command to run when the container starts
CMD ["uv", "run", "uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]