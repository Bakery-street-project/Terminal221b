# Terminal221b - Polymathic Autonomous Organization (PAO)
# Multi-stage build for minimal image size

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN pip install --no-cache-dir hatchling build

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY utils/ ./utils/

# Build wheel
RUN python -m build --wheel

# Runtime stage
FROM python:3.11-slim

LABEL org.opencontainers.image.title="Terminal221b"
LABEL org.opencontainers.image.description="Polymathic Autonomous Organization (PAO) - A sovereign, self-funding AI civilization engine"
LABEL org.opencontainers.image.source="https://github.com/Bakery-street-project/Terminal221b"
LABEL org.opencontainers.image.vendor="Bakery Street Project"
LABEL org.opencontainers.image.licenses="MIT"

# Create non-root user
RUN useradd --create-home --shell /bin/bash terminal221b

WORKDIR /app

# Copy wheel from builder
COPY --from=builder /build/dist/*.whl /tmp/

# Install the package
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Switch to non-root user
USER terminal221b

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color

# Default command
ENTRYPOINT ["terminal221b"]
CMD ["--help"]
