#!/bin/bash

# CallCenter Twisted - Convenience Script
# This script makes it easy to run the call center application

set -e

echo "CallCenter Twisted - Starting application..."

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Error: Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to start server
start_server() {
    echo "Starting callcenter server..."
    docker-compose up --build -d callcenter-server
    echo "Server started! Waiting for it to be ready..."
    sleep 3
}

# Function to start client
start_client() {
    echo "Starting callcenter client..."
    echo "You can now use commands like: call 1, answer A, reject B, hangup 1, quit"
    echo "=========================================="
    docker-compose run --rm callcenter-client
}

# Function to stop services
stop_services() {
    echo "Stopping all services..."
    docker-compose down
    echo "Services stopped."
}

# Function to show logs
show_logs() {
    echo "Showing server logs..."
    docker-compose logs -f callcenter-server
}

# Function to clean up
cleanup() {
    echo "Cleaning up containers and images..."
    docker-compose down --rmi all -v
    echo "Cleanup completed."
}

# Main script logic
case "${1:-start}" in
    start)
        check_docker
        start_server
        start_client
        ;;
    server)
        check_docker
        start_server
        echo "Server is running. Use './run.sh client' to start the client."
        ;;
    client)
        check_docker
        start_client
        ;;
    stop)
        stop_services
        ;;
    logs)
        show_logs
        ;;
    clean)
        cleanup
        ;;
    *)
        echo "Usage: $0 {start|server|client|stop|logs|clean}"
        echo ""
        echo "Commands:"
        echo "  start   - Start server and client (default)"
        echo "  server  - Start only the server"
        echo "  client  - Start only the client (requires server to be running)"
        echo "  stop    - Stop all services"
        echo "  logs    - Show server logs"
        echo "  clean   - Remove all containers and images"
        echo ""
        echo "Examples:"
        echo "  $0           # Start the full application"
        echo "  $0 start     # Start the full application"
        echo "  $0 server    # Start only the server"
        echo "  $0 client    # Start only the client"
        echo "  $0 stop      # Stop all services"
        exit 1
        ;;
esac
