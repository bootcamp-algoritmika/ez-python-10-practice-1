from abc import ABC, abstractmethod
from typing import List

from domain.user.dto import *
from domain.user.model import User


class UserServiceI(ABC):
    @abstractmethod
    def get_users(self, limit: int, offset: int) -> List[User]: pass

    @abstractmethod
    def get_user(self, user_id) -> User: pass

    @abstractmethod
    def create_user(self, user: CreateUserDTO) -> User: pass

    @abstractmethod
    def delete_user(self, user_id): pass

    @abstractmethod
    def update_user(self, user: UpdateUserDTO): pass

    @abstractmethod
    def partially_update(self, user: PartiallyUpdateUserDTO): pass
