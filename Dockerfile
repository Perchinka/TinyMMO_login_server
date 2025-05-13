FROM python:3.11-slim

# Ensure logs are output immediately
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN apt-get update \
    && apt-get install -y curl postgresql-client\
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

COPY . /app

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["python", "-m", "login_server"]
