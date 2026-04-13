from pydantic import BaseModel

class UserSchema(BaseModel):
    telegram_id: int
    username: str | None = None
    status: str = "common"