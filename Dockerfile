# Stage 1: Build dependencies
FROM python:3.12-slim-bookworm AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Final image
FROM python:3.12-slim-bookworm

LABEL version="v1.0.3"
LABEL description="Django Fullstack App with DevSecOps and Monitoring"
LABEL changes="Added Django management command for simulating user activity and generating test data"

# Create a non-privileged user to run the app
RUN addgroup --system django && adduser --system --group django

WORKDIR /app

# Set default environment variables for local testing
ENV DEBUG=True
ENV SECRET_KEY=django-insecure-default-key-change-me
ENV DATABASE_URL=sqlite:///db.sqlite3

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /wheels/*

# Copy project files
COPY . .

# Create directory for static and media files
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R django:django /app

# Switch to non-privileged user
USER django

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Default command (will be overridden by K8s for different processes like Celery)
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 voting_project.wsgi:application"]
