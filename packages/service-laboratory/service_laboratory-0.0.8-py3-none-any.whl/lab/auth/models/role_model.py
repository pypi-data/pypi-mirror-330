from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .auth_association_models import role_permission_association, user_role_association


class RoleModel(UUIDAuditBase):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    users = relationship(
        "UserModel",
        secondary=user_role_association,
        back_populates="roles",
        lazy="selectin",
    )
    permissions = relationship(
        "PermissionModel",
        secondary=role_permission_association,
        back_populates="roles",
        lazy="selectin",
    )
