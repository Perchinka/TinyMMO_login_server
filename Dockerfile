FROM python:3.11-slim

# Ensure logs are output immediately
ENV PYTHONUNBUFFERED=1

# Install Poetry for dependency management
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency declarations
COPY pyproject.toml poetry.lock /app/

# Install runtime dependencies only
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

# Copy application code
COPY . /app

# Default command to run the module
CMD ["python", "-m", "login_server"]
