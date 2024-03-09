from sqladmin import ModelView

from app.database.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.name, Users.surname]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
