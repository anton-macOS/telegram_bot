from models.user import Admin
from crud.crud_base import CRUDBase


class CRUDAdmin(CRUDBase):
    def __init__(self):
        super().__init__(Admin)


admin_crud = CRUDAdmin()