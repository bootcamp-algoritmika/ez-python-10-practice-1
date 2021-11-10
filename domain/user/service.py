from typing import List

from adapters.interfaces import UserServiceI
from domain.user.dto import CreateUserDTO, UpdateUserDTO, PartiallyUpdateUserDTO
from domain.user.model import User
from domain.user.storage import UserStorageI


class UserService(UserServiceI):
    def __init__(self, storage: UserStorageI):
        self.storage = storage

    def get_users(self, limit: int, offset: int) -> List[User]:
        # in real life any filters or something else
        users = self.storage.get_all(limit, offset)
        return users

    def get_user(self, user_id) -> User:
        users = self.storage.get_one(user_id=user_id)
        return users

    def create_user(self, user: CreateUserDTO) -> User:
        user = User(name=user.name, age=user.age)
        return self.storage.create(user=user)

    def delete_user(self, user_id) -> None:
        self.storage.delete(user_id=user_id)

    def update_user(self, user: UpdateUserDTO):
        user = User(id=user.id, name=user.name, age=user.age)
        self.storage.update(user=user)

    def partially_update(self, user: PartiallyUpdateUserDTO):
        old_user = self.get_user(user.id)
        if user.name is not None:
            old_user.name = user.name
        if user.age is not None:
            old_user.age = user.age

        self.storage.update(user=old_user)
