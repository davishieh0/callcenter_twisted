FROM debian:bookworm-slim

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv

# Activate virtual environment and install Twisted
RUN /opt/venv/bin/pip install twisted

# Create work directory
WORKDIR /app

# Copy client files
COPY client.py .

# Command to run client using virtual environment
CMD ["/opt/venv/bin/python", "client.py"]