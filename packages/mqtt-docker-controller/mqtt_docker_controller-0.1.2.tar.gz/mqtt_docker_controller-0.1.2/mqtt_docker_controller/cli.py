"""
Command Line Interface module for MQTT Manager.
Handles argument parsing and command routing.
"""

import argparse
import logging
from typing import Optional
from .config import MQTTConfig, MQTTCommand
from .client import MQTTClient
from .broker import DockerBroker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MQTTCommandLine:
    """
    Command Line Interface handler.
    Implements the Strategy pattern for different command operations.
    """
    def __init__(self):
        """Initialise CLI parser with all available commands."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the argument parser.
        
        Returns:
            argparse.ArgumentParser: Configured argument parser
        """
        # Create main parser
        parser = argparse.ArgumentParser(
            description="MQTT Manager - A tool for MQTT operations and broker management",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  Start broker:    mqtt_docker_controller start-broker
  Stop broker:     mqtt_docker_controller stop-broker
  Publish:         mqtt_docker_controller publish --broker localhost --topic test/topic --message "Hello"
  Subscribe:       mqtt_docker_controller subscribe --broker localhost --topic test/topic
            """
        )

        # Create command subparsers
        subparsers = parser.add_subparsers(
            dest="command",
            required=True,
            help="Available commands"
        )

        # Common arguments for MQTT operations
        common_args = argparse.ArgumentParser(add_help=False)
        common_args.add_argument(
            "--broker",
            type=str,
            required=True,
            help="MQTT Broker address"
        )
        common_args.add_argument(
            "--port",
            type=int,
            default=1883,
            help="MQTT Broker port (default: 1883)"
        )
        common_args.add_argument(
            "--client-id",
            type=str,
            default="mqtt_cli",
            help="MQTT Client ID (default: mqtt_cli)"
        )
        common_args.add_argument(
            "--qos",
            type=int,
            choices=[0, 1, 2],
            default=0,
            help="QoS level (default: 0)"
        )
        common_args.add_argument(
            "--keepalive",
            type=int,
            default=60,
            help="Keep-alive interval in seconds (default: 60)"
        )

        # Publish command
        publish_parser = subparsers.add_parser(
            "publish",
            parents=[common_args],
            help="Publish a message to a topic"
        )
        publish_parser.add_argument(
            "--topic",
            type=str,
            required=True,
            help="Topic to publish to"
        )
        publish_parser.add_argument(
            "--message",
            type=str,
            required=True,
            help="Message to publish"
        )
        publish_parser.add_argument(
            "--retain",
            action="store_true",
            help="Retain the message (default: False)"
        )

        # Subscribe command
        subscribe_parser = subparsers.add_parser(
            "subscribe",
            parents=[common_args],
            help="Subscribe to a topic"
        )
        subscribe_parser.add_argument(
            "--topic",
            type=str,
            required=True,
            help="Topic to subscribe to"
        )

        # Broker management commands
        subparsers.add_parser(
            "start-broker",
            help="Start a local MQTT broker in Docker"
        )
        subparsers.add_parser(
            "stop-broker",
            help="Stop the local MQTT broker"
        )

        return parser

    def parse_args(self) -> Optional[MQTTConfig]:
        """
        Parse command line arguments into configuration.
        
        Returns:
            Optional[MQTTConfig]: Configuration object or None for broker commands
        """
        args = self.parser.parse_args()

        # Return None for broker management commands
        if args.command in ['start-broker', 'stop-broker']:
            return None

        # Create MQTT configuration for client commands
        return MQTTConfig(
            broker=args.broker,
            port=args.port,
            client_id=args.client_id,
            qos=args.qos,
            keepalive=args.keepalive,
            topic=args.topic,
            message=getattr(args, 'message', None),
            retain=getattr(args, 'retain', False)
        )

def main() -> None:
    """
    Main entry point for the CLI application.
    Handles command routing and error management.
    """
    try:
        # Parse command line arguments
        cli = MQTTCommandLine()
        args = cli.parser.parse_args()

        # Handle broker management commands
        if args.command == "start-broker":
            broker = DockerBroker()
            broker.start_broker()
            return
        elif args.command == "stop-broker":
            broker = DockerBroker()
            broker.stop_broker()
            return

        # Handle MQTT client commands
        config = cli.parse_args()
        client = MQTTClient(config)
        client.connect()

        if args.command == "publish":
            client.publish()
        elif args.command == "subscribe":
            client.subscribe()

    except KeyboardInterrupt:
        logger.info("\nOperation interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()