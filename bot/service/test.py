from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.datastore.session import session_provider
from bot.models.test import Test
from bot.service.base import BaseService


async def get_test_service(
):
    session: AsyncSession = await session_provider()
    return TestService(Test, session)


class TestService(BaseService):
    pass
