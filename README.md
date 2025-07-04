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
## Docker Images
https://hub.docker.com/r/davishieh/callcenter-client
https://hub.docker.com/r/davishieh/callcenter-server
## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Running with Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/davishieh0/callcenter_twisted
cd callcenter_twisted/advanced_implementation  

# Start the application
docker compose run --rm callcenter-client
# The client will show an interactive prompt:
# (callCenter) 
```

## Available Commands

Once the client is running, you can use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `call <id>` | Make a call | `call 1` |
| `answer <operator_id>` | Answer a call | `answer A` |
| `reject <operator_id>` | Reject a call | `reject B` |
| `hangup <call_id>` | End a call | `hangup 1` |
| `quit` | Exit client | `quit` |


## Features

- **Call Routing**: Automatically assigns calls to available operators
- **Queue Management**: Queues calls when all operators are busy
- **Timeout Handling**: Automatically times out unanswered calls (10 seconds)
- **Multiple Operators**: Supports operators A and B
- **Real-time Updates**: Server sends status updates to client

## Development

### Running Locally (without Docker)

1. Install dependencies:
```bash
pip install twisted
```

2. Start server:
```bash
cd basic_implementation/advanced_implementation/server
python3 server.py
```

3. Start client:
```bash
cd basic_implementation/advanced_implementation/client
python3 client.py
```

### Building Docker Images

```bash
# Build server
docker build -t callcenter-server ./server

# Build client  
docker build -t callcenter-client ./client
```
