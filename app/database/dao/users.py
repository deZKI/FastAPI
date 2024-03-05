from app.database.dao.base import BaseDAO
from app.database.models.users import Users


class UsersDAO(BaseDAO):
    model = Users
