import logging
from pymongo.errors import ServerSelectionTimeoutError

from src.repository.inventory_repository import InventoryRepository

logger = logging.getLogger(__name__)


def seed_inventory_items(collection) -> None:
    try:
        repository = InventoryRepository(collection)

        if repository.count() > 0:
            return

        sample_items = [
            {
                "name": "Raspberry Pi 4",
                "description": "Single-board computer for embedded labs",
                "quantity": 25,
                "price": 85.50,
            },
            {
                "name": "Arduino Uno",
                "description": "Microcontroller board for prototyping",
                "quantity": 40,
                "price": 22.00,
            },
            {
                "name": "Projector HDMI Cable",
                "description": "2m HDMI cable for lecture halls",
                "quantity": 60,
                "price": 7.99,
            },
        ]

        for item in sample_items:
            repository.create(item)
    except ServerSelectionTimeoutError as e:
        logger.warning(f"Could not seed inventory: MongoDB connection failed. {str(e)}")
    except Exception as e:
        logger.error(f"Error seeding inventory: {str(e)}")
