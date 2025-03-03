# MQTT Docker Controller

A Python-based tool for managing MQTT operations and Docker-based MQTT brokers. This tool provides a unified interface for both MQTT client operations (publish/subscribe) and Docker-based Mosquitto broker management.

## Features

- 🐳 Docker-based MQTT broker management
  - Start/stop Mosquitto broker containers
  - Automatic configuration management
  - Container health monitoring
  - Automatic error detection and recovery
- 📨 MQTT client operations
  - Publish messages with configurable QoS and retain settings
  - Subscribe to topics with automatic reconnection
  - Support for multiple connection parameters
- 🛠️ Command-line interface
  - Simple, intuitive commands
  - Comprehensive help system
  - Error handling and logging

## Prerequisites

- Python 3.8 or higher
- Docker installed and running
  - macOS: Docker Desktop
  - Linux: Docker Engine
  - Windows: Docker Desktop
- Network access for MQTT operations
- Available ports:
  - 1883 (MQTT)
  - 9001 (WebSocket)

## Installation

```bash
# Install the package
pip install mqtt-docker-controller
```

## Usage

### Starting a Local MQTT Broker
```bash
# Start a new broker instance
mqtt-docker-controller start-broker

# Stop the running broker
mqtt-docker-controller stop-broker
```

### Publishing Messages
```bash
# Basic publish
mqtt-docker-controller publish --broker localhost --topic test/topic --message "Hello World"

# Publish with QoS and retain
mqtt-docker-controller publish \
    --broker localhost \
    --topic test/topic \
    --message "Hello World" \
    --qos 1 \
    --retain
```

### Subscribing to Topics
```bash
# Basic subscribe
mqtt-docker-controller subscribe --broker localhost --topic test/topic

# Subscribe with specific QoS
mqtt-docker-controller subscribe \
    --broker localhost \
    --topic test/topic \
    --qos 1
```

## Error Handling and Troubleshooting

### Docker-Related Issues

1. Docker Not Running
   ```
   ERROR: Docker daemon is not running
   Please start Docker with one of these commands:
     - macOS: open -a Docker
     - Linux: sudo systemctl start docker
     - Windows: Start Docker Desktop
   ```

2. Port Conflicts
   ```
   ERROR: Port 1883 or 9001 is already in use
   Please check if another broker or service is running on these ports
   ```

3. Image Issues
   - The tool will automatically attempt to pull the Mosquitto image if not found
   - Network issues during pull will be reported clearly

### MQTT-Related Issues

1. Connection Problems
   - Broker unreachable
   - Authentication failures
   - Invalid topic format

2. Common Fixes
   - Ensure Docker is running
   - Check port availability
   - Verify network connectivity
   - Confirm broker address is correct

## Configuration

### Default Broker Settings
- MQTT Port: 1883
- WebSocket Port: 9001
- Default Configuration Location: ~/mqtt-docker-controller-test/mosquitto.conf

### Client Settings
- Default QoS: 0
- Default Keep Alive: 60 seconds
- Auto-reconnect: Enabled

## Development

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/DylanWall96/mqtt-docker-controller.git
cd mqtt-docker-controller

# Install in development mode with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check code style
flake8 mqtt_docker_controller
black mqtt_docker_controller

# Type checking
mypy mqtt_docker_controller
```

### Project Structure
```
mqtt_docker_controller/
├── __init__.py         # Package initialisation
├── cli.py             # Command-line interface
├── broker.py          # Docker broker management
├── client.py          # MQTT client operations
├── config.py          # Configuration management
└── __main__.py        # Direct execution support
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Licence

This project is licensed under the MIT Licence - see the LICENCE file for details.