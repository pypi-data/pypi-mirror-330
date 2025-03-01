from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .auth_association_models import role_permission_association


class PermissionModel(UUIDAuditBase):
    __tablename__ = "permissions"

    app: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()

    roles = relationship(
        "RoleModel",
        secondary=role_permission_association,
        back_populates="permissions",
    )

    __table_args__ = (UniqueConstraint("app", "name", name="_permission_info"),)
