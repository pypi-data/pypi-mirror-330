"""
Docker MQTT Broker management module.
Handles starting, stopping, and managing the Mosquitto broker in a Docker container.
"""

import docker
from docker.errors import APIError, ImageNotFound
import time
import logging
from typing import Optional
from .config import BrokerConfig

# Configure logging for the broker module
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DockerBroker:
    """
    Manages the Docker MQTT broker container.
    Implements the Singleton pattern to ensure only one broker instance exists.
    """
    # Singleton instance
    _instance: Optional['DockerBroker'] = None
    
    def __new__(cls) -> 'DockerBroker':
        """
        Create or return the singleton instance of DockerBroker.
        Ensures only one broker manager exists.
        """
        if cls._instance is None:
            cls._instance = super(DockerBroker, cls).__new__(cls)
            cls._instance.client = docker.from_env()
            cls._instance.container = None
        return cls._instance

    def _create_config(self) -> str:
        """
        Create and write the Mosquitto configuration file.
        
        Returns:
            str: Path to the configuration file
        
        Raises:
            IOError: If unable to write configuration file
        """
        try:
            config_path = BrokerConfig.get_config_path()
            config_path.write_text(BrokerConfig.get_config_content())
            logger.debug(f"Created config file at {config_path}")
            return str(config_path)
        except IOError as e:
            logger.error(f"Failed to create config file: {e}")
            raise

    def start_broker(self, timeout: int = 30) -> None:
        """
        Start the MQTT broker container.
        
        Args:
            timeout (int): Maximum time to wait for broker startup in seconds
            
        Raises:
            TimeoutError: If broker doesn't start within timeout period
            ConnectionError: If Docker daemon is not running
            docker.errors.DockerException: If Docker operations fail
        """
        try:
            # First check if Docker is running
            self._check_docker_running()
            
            # Stop any existing broker container
            self.stop_broker()
            
            # Create configuration
            config_path = self._create_config()
            
            # Configure container settings
            container_config = {
                'name': BrokerConfig.CONTAINER_NAME,
                'ports': {
                    f'{BrokerConfig.MQTT_PORT}/tcp': BrokerConfig.MQTT_PORT,
                    f'{BrokerConfig.WEBSOCKET_PORT}/tcp': BrokerConfig.WEBSOCKET_PORT
                },
                'volumes': {
                    config_path: {
                        'bind': '/mosquitto/config/mosquitto.conf',
                        'mode': 'ro'
                    }
                },
                'detach': True
            }
            
            # Start container
            logger.info("Starting MQTT broker container...")
            self.container = self.client.containers.run(
                BrokerConfig.IMAGE_NAME,
                **container_config
            )
            
            # Wait for container to be ready
            self._wait_for_broker(timeout)
            
            logger.info("""
    MQTT broker is running.
    Usage:
        Subscribe: mosquitto_sub -h localhost -t test/topic
        Publish:   mosquitto_pub -h localhost -t test/topic -m "Your message"
        Stop:      Use the stop-broker command
    """)
            
        except docker.errors.ImageNotFound:
            logger.error(f"Docker image {BrokerConfig.IMAGE_NAME} not found. Attempting to pull...")
            try:
                self.client.images.pull(BrokerConfig.IMAGE_NAME)
                # Retry starting the broker
                return self.start_broker(timeout)
            except Exception as e:
                logger.error(f"Failed to pull Docker image: {e}")
                raise
                
        except docker.errors.APIError as e:
            if "port is already allocated" in str(e):
                logger.error(f"Port {BrokerConfig.MQTT_PORT} or {BrokerConfig.WEBSOCKET_PORT} is already in use")
                logger.error("Please check if another broker or service is running on these ports")
            raise
            
        except Exception as e:
            logger.error(f"Failed to start MQTT broker: {e}")
            self.stop_broker()
            raise

    def _wait_for_broker(self, timeout: int) -> None:
        """
        Wait for broker container to be ready.
        
        Args:
            timeout (int): Maximum time to wait in seconds
        
        Raises:
            TimeoutError: If broker isn't ready within timeout period
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                container = self.client.containers.get(BrokerConfig.CONTAINER_NAME)
                if container.status == 'running':
                    # Additional check could be added here to verify MQTT port is responding
                    return
            except docker.errors.NotFound:
                pass
            time.sleep(1)
        
        raise TimeoutError(f"Failed to start MQTT broker within {timeout} seconds")

    def stop_broker(self) -> None:
        """
        Stop and remove the MQTT broker container.
        Handles cleanup of Docker resources.
        """
        try:
            container = self.client.containers.get(BrokerConfig.CONTAINER_NAME)
            logger.info("Stopping MQTT broker...")
            container.stop()
            logger.info("Removing container...")
            container.remove()
            logger.info("MQTT broker stopped and removed.")
        except docker.errors.NotFound:
            logger.debug("No existing broker container found.")
        except Exception as e:
            logger.error(f"Error stopping MQTT broker: {e}")
            raise

    def get_broker_status(self) -> str:
        """
        Get the current status of the broker container.
        
        Returns:
            str: Current status of the broker ('running', 'stopped', or 'not found')
        """
        try:
            container = self.client.containers.get(BrokerConfig.CONTAINER_NAME)
            return container.status
        except docker.errors.NotFound:
            return "not found"
        except Exception as e:
            logger.error(f"Error getting broker status: {e}")
            return "error"
        
    def _check_docker_running(self) -> None:
        """
        Check if Docker daemon is running.
        
        Raises:
            ConnectionError: If Docker daemon is not running
        """
        try:
            self.client.ping()
        except Exception as e:
            logger.error("Docker daemon is not running")
            logger.error("Please start Docker with one of these commands:")
            logger.error("  - macOS: open -a Docker")
            logger.error("  - Linux: sudo systemctl start docker")
            logger.error("  - Windows: Start Docker Desktop")
            raise ConnectionError("Docker daemon is not running. Please start Docker first.") from e