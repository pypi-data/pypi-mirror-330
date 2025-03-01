from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .auth_association_models import user_role_association


class UserModel(UUIDAuditBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column()

    roles = relationship(
        "RoleModel",
        secondary=user_role_association,
        back_populates="users",
        lazy="selectin",
    )
