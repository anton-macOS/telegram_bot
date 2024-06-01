
from models.user import User
from crud.crud_base import CRUDBase


class CRUDUser(CRUDBase):
    def __init__(self):
        super().__init__(User)


user_crud = CRUDUser()