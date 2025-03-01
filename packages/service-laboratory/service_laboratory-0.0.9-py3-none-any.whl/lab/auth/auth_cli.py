import os

import click
import yaml

from ..core.cli import coro
from ..core.database import session_maker
from .auth_core import hash_password
from .models import PermissionModel, RoleModel, UserModel
from .repositories.permission_repository import provide_permission_repository
from .repositories.role_repository import provide_role_repository
from .repositories.user_repository import provide_user_repository


@click.group()
def auth_cli(): ...

@auth_cli.command()
@coro
async def load_auth():
    async with session_maker() as session:
        permission_repository = provide_permission_repository(session)
        role_repository = provide_role_repository(session)
        user_repository = provide_user_repository(session)

        await permission_repository.delete_where(auto_commit=True)
        await role_repository.delete_where(auto_commit=True)
        await user_repository.delete_where(auto_commit=True)

        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "./fixtures/auth.yaml"), "r"
        ) as stream:
            data_loaded = yaml.safe_load(stream)
            permissions = await permission_repository.add_many(
                [
                    PermissionModel(app=app, name=name)
                    for app, names in data_loaded.get("permissions").items()
                    for name in names
                ],
                auto_commit=True,
            )

            roles = []
            for name, permission_values in data_loaded.get("roles").items():
                role = RoleModel(name=name)
                role_permission_filter = {
                    app: {name for name in names}
                    for app, names in permission_values.items()
                }
                for permission in permissions:
                    if permission.name in role_permission_filter.get(permission.app):
                        role.permissions.append(permission)
                roles.append(role)

            await role_repository.add_many(roles, auto_commit=True)

            users = []

            for user_data in data_loaded.get("users"):
                email = user_data.get("email")
                users_roles = {role for role in user_data.get("roles")}

                user = UserModel(email=email, password=hash_password("password"))
                for role in roles:
                    if role.name in users_roles:
                        user.roles.append(role)
                users.append(user)

            await user_repository.add_many(users, auto_commit=True)
