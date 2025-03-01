import uuid
from typing import List

import msgspec
from litestar import Controller, get

from ..repositories import (
    RoleRepository,
    provide_role_repository,
)


class Permission(msgspec.Struct):
    id: uuid.UUID
    app: str
    name: str


class Role(msgspec.Struct):
    id: uuid.UUID
    name: str
    permissions: List[Permission]


class RoleController(Controller):
    dependencies = {"role_repository": provide_role_repository}

    path = "/roles"

    @get(path="/")
    async def get_list(self, role_repository: RoleRepository) -> List[Role]:
        roles = await role_repository.list()

        return [
            Role(
                id=role.id,
                name=role.name,
                permissions=[
                    Permission(
                        id=permission.id, name=permission.name, app=permission.app
                    )
                    for permission in role.permissions
                ],
            )
            for role in roles
        ]
