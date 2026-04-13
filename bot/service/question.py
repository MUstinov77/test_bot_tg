from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import random

from bot.core.datastore.session import session_provider
from bot.models.question import Question
from bot.service.base import BaseService


async def get_question_service():
    session: AsyncSession = await session_provider()
    return QuestionService(Question, session)

class QuestionService(BaseService):

    async def get_random_question(self, test_id: int):
        query = (
            select(self.model).
            where(self.model.test_id == test_id).
            order_by(random()).
            limit(1)
        )
        result = await self.session.execute(query)
        question = result.scalar_one_or_none()
        await self.session.close()
        return question