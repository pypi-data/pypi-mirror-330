"""
Main entry point for the MQTT Manager package.
Allows running the package directly using 'python -m mqtt_docker_controller'.
"""

import sys
import logging
from .cli import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nOperation interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)