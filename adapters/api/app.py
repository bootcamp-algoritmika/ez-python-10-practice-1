from wsgiref import simple_server

import falcon
from falcon import App

from adapters.api.controllers import UsersResource, UserResource
from adapters.db.user.storage import UserStorage
from domain.user.service import UserService

storage = UserStorage()
service = UserService(storage=storage)


def create_app() -> App:
    app = falcon.App()

    users_view = UsersResource(service=service)
    user_view = UserResource(service=service)

    app.add_route('/users/', users_view)
    app.add_route('/users/{user_id}', user_view)
    return app


if __name__ == '__main__':
    app = create_app()
    httpd = simple_server.make_server('127.0.0.1', 1234, app)
    httpd.serve_forever()

