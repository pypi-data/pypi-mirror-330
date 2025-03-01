from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import RoleModel, UserModel, user_role_association


class UserRepository(SQLAlchemyAsyncRepository):
    model_type = UserModel

    async def create_admin(
        self,
        user: UserModel,
    ) -> UserModel:
        user = await self.add(user, auto_commit=True)
        return await self.add_user_role(
            user,
            "admin",
        )

    async def add_user_role(
        self,
        user: UserModel,
        role_name: str,
    ) -> UserModel:
        role = await self.session.scalar(select(RoleModel).where(RoleModel.name == role_name))
        await self.session.execute(insert(user_role_association).values(user_id=user.id, role_id=role.id))

        await self.session.commit()
        return user


def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)
