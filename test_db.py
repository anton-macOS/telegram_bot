import os
import logging
from sqlalchemy.orm import Session
from db.dependencies import get_db_dependency
from crud.user import user_crud
from db.session import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        test_user_data = {
            "full_name": "Test User",
            "city": "Test City",
            "country": "Test Country",
            "phone": "+1234567890",
            "birth_date": "2000-01-01",
            "email": "test@example.com",
            "discord_nick": "test_discord",
            "postal_address": "Test Address",
            "adaptation_start_date": "2024-01-01",
            "work_start_date": None,
            "assigned_stream": None,
            "dismissal_date": None,
            "admin_id": None,
            "work_tg_nick": "test_work_tg_nick",
            "personal_tg_nick": "test_personal_tg_nick",
            "photo": "path/to/test_photo.jpg"
        }

        new_user = user_crud.create(db=db, obj_in=test_user_data)
        logger.info(f"User created: {new_user}")
        print(f"Created user: {new_user.full_name}, email: {new_user.email}")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
    finally:
        next(db_gen, None)

if __name__ == '__main__':
    main()