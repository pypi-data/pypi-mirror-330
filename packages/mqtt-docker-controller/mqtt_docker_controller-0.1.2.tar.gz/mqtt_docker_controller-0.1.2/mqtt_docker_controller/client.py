"""
MQTT Client module.
Handles MQTT client operations including connections, publishing, and subscribing.
"""

import paho.mqtt.client as mqtt
import logging
from typing import Callable, Dict, List
from collections import defaultdict
from queue import Queue
from .config import MQTTConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MQTTCallback:
    """
    Callback handler for MQTT events.
    Implements the Observer pattern for MQTT events.
    """
    def __init__(self):
        """Initialise callback handler with message queue and event handlers."""
        self.message_queue: Queue = Queue()
        self.handlers: Dict[str, List[Callable]] = defaultdict(list)

    def on_connect(self, client, userdata, flags, rc: int) -> None:
        """
        Callback for client connection events.
        
        Args:
            client: MQTT client instance
            userdata: User-defined data
            flags: Response flags from broker
            rc (int): Connection result code
        """
        if rc == 0:
            logger.info("Connected to MQTT broker successfully!")
        else:
            logger.error(f"Failed to connect, return code: {rc}")
        self._notify('connect', rc)

    def on_disconnect(self, client, userdata, rc: int) -> None:
        """
        Callback for client disconnection events.
        
        Args:
            client: MQTT client instance
            userdata: User-defined data
            rc (int): Disconnection reason code
        """
        if rc == 0:
            logger.info("Disconnected from broker successfully")
        else:
            logger.warning(f"Unexpected disconnection, code: {rc}")
        self._notify('disconnect', rc)

    def on_message(self, client, userdata, msg) -> None:
        """
        Callback for received messages.
        
        Args:
            client: MQTT client instance
            userdata: User-defined data
            msg: Received message object
        """
        message_info = {
            'topic': msg.topic,
            'payload': msg.payload.decode(),
            'qos': msg.qos
        }
        self.message_queue.put(message_info)
        logger.info(
            f"Received message: '{message_info['payload']}' "
            f"on topic '{message_info['topic']}'"
        )
        self._notify('message', message_info)

    def on_publish(self, client, userdata, mid) -> None:
        """
        Callback for successful message publications.
        
        Args:
            client: MQTT client instance
            userdata: User-defined data
            mid: Message ID
        """
        logger.debug(f"Message {mid} published successfully")
        self._notify('publish', mid)

    def add_handler(self, event: str, handler: Callable) -> None:
        """
        Register a new event handler.
        
        Args:
            event (str): Event type to handle
            handler (Callable): Handler function
        """
        self.handlers[event].append(handler)

    def _notify(self, event: str, data) -> None:
        """
        Notify all registered handlers of an event.
        
        Args:
            event (str): Event type that occurred
            data: Event-related data
        """
        for handler in self.handlers[event]:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")

class MQTTClient:
    """
    Main MQTT Client class.
    Implements the Facade pattern for MQTT operations.
    """
    def __init__(self, config: MQTTConfig):
        """
        Initialise MQTT client with configuration.
        
        Args:
            config (MQTTConfig): Client configuration
        """
        self.config = config
        self.callback_handler = MQTTCallback()
        self.client = mqtt.Client(client_id=config.client_id)
        self._setup_callbacks()

    def _setup_callbacks(self) -> None:
        """Configure client callbacks."""
        self.client.on_connect = self.callback_handler.on_connect
        self.client.on_disconnect = self.callback_handler.on_disconnect
        self.client.on_message = self.callback_handler.on_message
        self.client.on_publish = self.callback_handler.on_publish

    def connect(self) -> None:
        """
        Connect to the MQTT broker.
        
        Raises:
            ConnectionError: If connection fails
        """
        try:
            self.client.connect(
                self.config.broker,
                self.config.port,
                self.config.keepalive
            )
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise ConnectionError(f"Failed to connect to broker: {e}")

    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        self.client.disconnect()

    def publish(self) -> None:
        """
        Publish a message to a topic.
        
        Raises:
            ValueError: If message is not provided
        """
        if not self.config.message:
            raise ValueError("Message is required for publishing")

        self.client.loop_start()
        try:
            result = self.client.publish(
                topic=self.config.topic,
                payload=self.config.message,
                qos=self.config.qos,
                retain=self.config.retain
            )
            result.wait_for_publish()
            logger.info(
                f"Published message '{self.config.message}' "
                f"to topic '{self.config.topic}'"
            )
        finally:
            self.client.loop_stop()

    def subscribe(self) -> None:
        """Subscribe to a topic and start message loop."""
        try:
            self.client.subscribe(self.config.topic, qos=self.config.qos)
            logger.info(
                f"Subscribed to topic '{self.config.topic}' "
                f"with QoS {self.config.qos}"
            )
            self.client.loop_forever()
        except KeyboardInterrupt:
            logger.info("Subscription interrupted by user")
            self.disconnect()
        except Exception as e:
            logger.error(f"Subscription error: {e}")
            self.disconnect()
            raise