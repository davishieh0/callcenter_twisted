# CallCenter Twisted

A call center simulation using Python Twisted framework with TCP client-server architecture.

## Project Description

This project implements a call center management system where:
- **Server**: Manages operators, call queues, and call states
- **Client**: Command-line interface for call center operations
- **Features**: Call routing, timeout handling, queue management

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  Server         │         │  Client         │
│  Container      │◄────────│  Container      │
│                 │  TCP    │                 │
│  - server.py    │  :5678  │  - client.py    │
│  - logic.py     │         │  - cmd prompt   │
│  - schemas.py   │         │                 │
└─────────────────┘         └─────────────────┘
```

### Running with Docker Compose (Recommended)

```bash
# 1. Clone the repository and navigate to the directory
git clone https://github.com/davishieh0/callcenter_twisted
cd callcenter_twisted/advanced_implementation  

# 2. Build and start containers in the background
docker compose up --build -d

# 3. Start the server
docker exec -it callcenter-server /opt/venv/bin/python server.py

# 4. In a new terminal, start the client
docker exec -it callcenter-client /opt/venv/bin/python client.py
```