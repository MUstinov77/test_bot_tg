from core.datastore.session import session_provider
from models.user import User
from service.base import BaseService

async def get_user_service():
    session = await session_provider()
    return UserService(User, session)

class UserService(BaseService):

    pass