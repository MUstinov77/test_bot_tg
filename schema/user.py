from pydantic import BaseModel

class UserSchema(BaseModel):
    telegram_id: int
    username: str
    status: str = "common"