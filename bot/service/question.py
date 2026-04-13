from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import random

from core.datastore.session import session_provider
from models.question import Question
from service.base import BaseService


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