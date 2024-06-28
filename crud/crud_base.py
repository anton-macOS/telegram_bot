from typing import Any, List, Type, TypeVar, Optional, Union, Dict

from sqlalchemy.orm import Session
from pydantic import EmailStr
from sqlalchemy.ext.declarative import as_declarative

ModelType = TypeVar("ModelType", bound=as_declarative())


class CRUDBase:
    """Class for CRUD operations on database models."""

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get object by id."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all objects."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_user_by_email(self, db: Session, email: EmailStr) -> Optional[ModelType]:
        """Get user by email."""
        return db.query(self.model).filter(self.model.email == email).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[ModelType]:
        """Get user by username"""
        user = db.query(self.model).filter(self.model.personal_tg_nick == username).first()
        return user if user else None

    def get_users_by_two_cols(self, db: Session, username: str) -> Optional[ModelType]:
        user = db.query(self.model).filter(self.model.personal_tg_nick == username).first()
        if not user:
            user = db.query(self.model).filter(self.model.work_tg_nick == username).first()
        return user if user else None

    def get_field_by_username(self, db: Session, username: str, field: str) -> Any:
        """Get field by username"""
        obj = db.query(self.model).filter(self.model.personal_tg_nick == username).first()
        return getattr(obj, field) if obj else None

    def get_users_by_admin_id(self, db: Session, admin_id: int) -> List[ModelType]:
        """Get users by admin ID"""
        return db.query(self.model).filter(self.model.admin_id == admin_id).all()

    def get_all_chat_ids(self, db: Session) -> List[int]:
        """Get all chat ids from user and admin tabs"""
        return [chat_id for (chat_id,) in db.query(self.model.chat_id).all()]

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """Create object."""
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Update object."""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Remove object."""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
