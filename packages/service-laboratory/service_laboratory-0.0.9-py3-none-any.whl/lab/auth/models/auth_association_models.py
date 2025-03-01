from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Column, ForeignKey, Table

user_role_association = Table(
    "users_roles",
    UUIDAuditBase.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE")),
)

role_permission_association = Table(
    "roles_permissions",
    UUIDAuditBase.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE")),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE")),
)
