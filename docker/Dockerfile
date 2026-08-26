# syntax=docker/dockerfile:1

# Build production Python dependencies in an isolated environment.
FROM python:3.11-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN python -m venv "${VIRTUAL_ENV}"

WORKDIR /build

# Copy dependency definitions separately to preserve Docker build cache
# when only application source code changes.
COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    -r requirements.txt


# Create the runtime image containing only the application requirements.
FROM python:3.11-slim AS runtime

# Disable bytecode generation and emit application logs immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}"

# Use a dedicated unprivileged account to run the application.
RUN groupadd --gid 10001 appuser \
    && useradd \
        --uid 10001 \
        --gid 10001 \
        --no-create-home \
        --shell /usr/sbin/nologin \
        appuser

WORKDIR /app

# Reuse the Python environment prepared during the build stage.
COPY --from=builder /opt/venv /opt/venv

# Copy only application source code and assign it to the runtime user.
COPY --chown=10001:10001 app ./app

USER 10001:10001

# Document the port exposed by Uvicorn inside the container.
EXPOSE 8000

# Run Uvicorn as the container's main process.
ENTRYPOINT ["python", "-m", "uvicorn"]

# Default server configuration. HTTP access logging is handled
# by the application's logging middleware.
CMD ["app.main:app", "--host", "0.0.0.0", "--no-access-log"]