"""
Configuration module for MQTT Manager.
Contains data classes and enums for configuration management.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
import pathlib

class MQTTCommand(Enum):
    """
    Enumeration of available MQTT commands.
    Using Enum ensures type safety and clear command definitions.
    """
    PUBLISH = auto()      # Command for publishing messages
    SUBSCRIBE = auto()    # Command for subscribing to topics
    START_BROKER = auto() # Command for starting the Docker broker
    STOP_BROKER = auto()  # Command for stopping the Docker broker

@dataclass
class MQTTConfig:
    """
    Data class for MQTT configuration settings.
    Uses Python's dataclass for automatic initialiation and representation.
    
    Attributes:
        broker (str): The MQTT broker address
        port (int): The broker port number (default: 1883)
        client_id (str): Unique identifier for the MQTT client
        qos (int): Quality of Service level (0, 1, or 2)
        keepalive (int): Connection keepalive interval in seconds
        topic (str): MQTT topic for publish/subscribe operations
        message (Optional[str]): Message content for publish operations
        retain (bool): Whether to retain published messages
    """
    broker: str
    port: int = 1883
    client_id: str = "mqtt_cli"
    qos: int = 0
    keepalive: int = 60
    topic: str = ""
    message: Optional[str] = None
    retain: bool = False

class BrokerConfig:
    """
    Configuration settings for the Docker MQTT broker.
    Uses class attributes for shared broker settings.
    """
    # Docker container configuration
    CONTAINER_NAME: str = "mqtt-broker"
    IMAGE_NAME: str = "eclipse-mosquitto:latest"
    
    # Port mappings
    MQTT_PORT: int = 1883
    WEBSOCKET_PORT: int = 9001
    
    # Default broker configuration
    DEFAULT_CONFIG: str = """
    listener 1883
    protocol mqtt
    allow_anonymous true
    log_type all
    log_timestamp true
    connection_messages true
    listener 9001
    protocol websockets
    """
    
    @classmethod
    def get_config_path(cls) -> pathlib.Path:
        """
        Get the path for the Mosquitto configuration file.
        Creates the directory if it doesn't exist.
        
        Returns:
            pathlib.Path: Path to the configuration file
        """
        test_dir = pathlib.Path.home() / "mqtt_docker_controller-test"
        test_dir.mkdir(parents=True, exist_ok=True)
        return test_dir / "mosquitto.conf"

    @classmethod
    def get_config_content(cls) -> str:
        """
        Get the configuration content for the Mosquitto broker.
        
        Returns:
            str: Configuration file content
        """
        return cls.DEFAULT_CONFIG.strip()