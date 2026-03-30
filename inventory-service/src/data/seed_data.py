import logging
from pymongo.errors import ServerSelectionTimeoutError

from src.repository.inventory_repository import InventoryRepository

logger = logging.getLogger(__name__)


def seed_inventory_items(collection) -> None:
    try:
        repository = InventoryRepository(collection)

        if repository.count() > 0:
            logger.info("Seed data skipped: inventory collection already contains data.")
            return

        sample_items = [
            {
                "name": "Raspberry Pi 4",
                "description": "Single-board computer for embedded labs",
                "quantity": 25,
                "price": 85.50,
                "supplier": "Raspberry Supplier",
                "condition": "New",
                "warranty_period": "2 years",
            },
            {
                "name": "Arduino Uno",
                "description": "Microcontroller board for prototyping",
                "quantity": 40,
                "price": 22.00,
                "supplier": "Arduino Supplier",
                "condition": "New",
                "warranty_period": "1 year",
            },
            {
                "name": "Projector HDMI Cable",
                "description": "2m HDMI cable for lecture halls",
                "quantity": 60,
                "price": 7.99,
                "supplier": "Cable Supplier",
                "condition": "New",
                "warranty_period": "6 months",
            },
        ]

        for item in sample_items:
            repository.create(item)
        logger.info("Seed data inserted into inventory collection.")
    except ServerSelectionTimeoutError as e:
        logger.warning(f"Could not seed inventory: MongoDB connection failed. {str(e)}")
    except Exception as e:
        logger.error(f"Error seeding inventory: {str(e)}")
