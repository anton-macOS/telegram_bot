from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from db.session import get_db


async def get_db_dependency(callback: CallbackQuery) -> Session:
    """Get database session dependency for callback query handler."""
    db_gen = get_db()
    db: Session = next(db_gen)
    try:
        yield db
    finally:
        next(db_gen, None)