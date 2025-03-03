"""
MQTT Manager Package.
A comprehensive tool for MQTT operations and broker management.

This package provides:
- MQTT client operations (publish/subscribe)
- Docker-based MQTT broker management
- Command-line interface
"""

# Version of the mqtt_docker_controller package
__version__ = '0.1.2'

# Import main components for easy access
from .client import MQTTClient
from .broker import DockerBroker
from .config import MQTTConfig, MQTTCommand
from .cli import main

# Define what should be available when using "from mqtt_docker_controller import *"
__all__ = [
    'MQTTClient',
    'DockerBroker',
    'MQTTConfig',
    'MQTTCommand',
    'main',
]

# Package metadata
__author__ = 'Dylan Wall'
__email__ = ''
__description__ = 'A comprehensive and handy MQTT management tool'