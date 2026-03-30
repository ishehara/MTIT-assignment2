import logging
from pymongo.errors import ServerSelectionTimeoutError

from ..repository.staff_repository import StaffRepository

logger = logging.getLogger(__name__)


def seed_staff_data(collection) -> None:
    try:
        repository = StaffRepository(collection)

        if repository.count() > 0:
            return

        sample_staff = [
            {
                "name": "Ashan Perera",
                "phone": "0711234567",
                "email": "ashan@repairshop.lk",
                "specialty": "MacBook Expert",
                "status": "active",
            },
            {
                "name": "Nimasha Silva",
                "phone": "0729876543",
                "email": "nimasha@repairshop.lk",
                "specialty": "Screen Repair",
                "status": "active",
            },
            {
                "name": "Kasun Fernando",
                "phone": "0765554433",
                "email": "kasun@repairshop.lk",
                "specialty": "Water Damage Recovery",
                "status": "active",
            },
        ]

        for staff in sample_staff:
            repository.create(staff)
    except ServerSelectionTimeoutError as e:
        logger.warning(f"Could not seed staff: MongoDB connection failed. {str(e)}")
    except Exception as e:
        logger.error(f"Error seeding staff: {str(e)}")
