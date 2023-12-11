##### Base Stage #####
FROM python:3.12-slim-bookworm as base

# Set default path
ENV PATH="/app/.venv/bin:${PATH}"

##### Builder Stage #####
FROM base as builder

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
COPY templates ./templates
COPY static ./static

##### Final Stage #####
FROM base

# Copy content from builder stage
COPY --from=builder /app /app

# Add qrcode user and create directories
RUN useradd -m qrcode

# Set permissions
RUN chown -R qrcode:qrcode /app

# Set workdir and user
WORKDIR /app
USER qrcode

# Expose port
EXPOSE 8000

# Set entrypoint and cmd
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "secure_qrcode.api:app"]
