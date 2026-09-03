# syntax=docker/dockerfile:1

# Install production Python dependencies in an isolated build stage.
FROM python:3.11-slim AS builder

WORKDIR /build

# Copy dependency definitions separately to preserve Docker build cache
# when only application source code changes.
COPY requirements.txt .

# Install only the application runtime dependencies into a separate directory.
RUN python -m pip install \
    --no-cache-dir \
    --target /install \
    -r requirements.txt


# Create the runtime image containing only what is required to run the application.
FROM python:3.11-slim AS runtime

# Disable bytecode generation and emit application logs immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Apply available Debian security updates and remove Python packaging tools
# that are not required at runtime.
RUN apt-get update \
    && apt-get upgrade -y \
    && python -m pip uninstall -y setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

# Use a dedicated unprivileged account to run the application.
RUN groupadd --gid 10001 appuser \
    && useradd \
        --uid 10001 \
        --gid 10001 \
        --no-create-home \
        --shell /usr/sbin/nologin \
        appuser

WORKDIR /app

# Copy only the application dependencies prepared during the build stage.
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

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