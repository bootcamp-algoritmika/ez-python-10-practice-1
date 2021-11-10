import json

import falcon

from adapters.interfaces import UserServiceI
from domain.user.dto import UpdateUserDTO, PartiallyUpdateUserDTO, CreateUserDTO
from domain.user.exceptions import UserNotFoundException


class UserResource:
    def __init__(self, service: UserServiceI):
        self.service = service

    def on_get(self, req, resp, user_id):
        try:
            user = self.service.get_user(user_id=user_id)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.body = json.dumps(user.__dict__)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, user_id):
        updated_user = req.media
        if "id" not in updated_user:
            updated_user["id"] = user_id
        dto = UpdateUserDTO(**updated_user)
        try:
            self.service.update_user(dto)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, user_id):
        patched_user = req.media
        if "id" not in patched_user:
            patched_user["id"] = user_id
        dto = PartiallyUpdateUserDTO(**patched_user)
        try:
            self.service.partially_update(dto)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, user_id):
        try:
            self.service.delete_user(user_id)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class UsersResource:
    def __init__(self, service: UserServiceI):
        self.service = service

    def on_get(self, req, resp):
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0
        users = self.service.get_users(limit=limit, offset=offset)
        # или сериализация с помощью pydantic/marshmallow
        # pydantic - быстрее и интерфейс попроще
        res = []
        for u in users:
            res.append(u.__dict__)
        resp.body = json.dumps(res)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.get_media()
        new_user = CreateUserDTO(**data)
        user = self.service.create_user(new_user)
        resp.status = falcon.HTTP_201
        resp.location = f'/users/{user.id}'
