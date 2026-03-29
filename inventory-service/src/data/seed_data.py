from src.repository.inventory_repository import InventoryRepository


def seed_inventory_items(collection) -> None:
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
