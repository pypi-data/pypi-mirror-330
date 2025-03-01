import uuid
from typing import List

import msgspec
from litestar import Controller, get

from ..repositories import (
    UserRepository,
    provide_user_repository,
)


class PermissionRole(msgspec.Struct):
    id: uuid.UUID
    name: str


class Permission(msgspec.Struct):
    id: uuid.UUID
    name: str
    app: str


class Role(msgspec.Struct):
    id: uuid.UUID
    name: str
    permissions: List[Permission]


class User(msgspec.Struct):
    id: uuid.UUID
    email: str
    roles: List[Role]


class UserController(Controller):
    dependencies = {"user_repository": provide_user_repository}

    path = "/users"

    @get(path="/", exclude_from_auth=True)
    async def get_list(self, user_repository: UserRepository) -> List[User]:
        users = await user_repository.list()

        return [
            User(
                id=user.id,
                email=user.email,
                roles=[
                    Role(
                        id=role.id,
                        name=role.name,
                        permissions=[
                            Permission(
                                id=permission.id,
                                name=permission.name,
                                app=permission.app,
                            )
                            for permission in role.permissions
                        ],
                    )
                    for role in user.roles
                ],
            )
            for user in users
        ]
