from bot.core.datastore.session import session_provider
from bot.models.user import User
from bot.service.base import BaseService

async def get_user_service():
    session = await session_provider()
    return UserService(User, session)

class UserService(BaseService):

    pass