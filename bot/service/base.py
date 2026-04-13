from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:

    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_scalar_by_field(
            self,
            field_name,
            field_value,
    ):
        query = (
            select(self.model).
            where(field_name == field_value)
        )
        result = await self.session.execute(query)
        scalar = result.scalar_one_or_none()
        await self.session.close()
        return scalar

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        rows = result.scalars().all()
        await self.session.close()
        return rows

    async def create(self, data: dict):
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def create_instance(self, data: dict):
        try:
            obj = await self.create(data)
            return obj
        except SQLAlchemyError as e:
                await self.session.rollback()
        finally:
            await self.session.close()