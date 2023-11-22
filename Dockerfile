##### Builder Stage #####
FROM python:3.12-slim-bookworm as builder

# Set default path
ENV PATH="/app/.venv/bin:${PATH}"

# Set default workdir
WORKDIR /app

# Create virtualenv and install Python packages
RUN pip install --no-cache-dir pip -U && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.in-project true
COPY ./poetry.lock poetry.lock
COPY ./pyproject.toml pyproject.toml
RUN poetry install --only main

# Copy app files to workdir
COPY secure_qrcode ./secure_qrcode

##### Final Stage #####
FROM python:3.12-slim-bookworm

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Set default path
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH /app

# Copy content from builder stage
COPY --from=builder /app /app

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add qrcode user and create directories
RUN useradd -m qrcode && mkdir -p /app

# Set permissions
RUN chown -R qrcode:qrcode /app

# Set workdir and user
WORKDIR /app
USER qrcode

# Expose port
EXPOSE 8000

# Set entrypoint and cmd
ENTRYPOINT ["/usr/bin/tini", "--", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "secure_qrcode.api:app"]
