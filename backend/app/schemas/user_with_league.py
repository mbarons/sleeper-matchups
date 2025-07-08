from pydantic import BaseModel

from app.schemas import League, User


class UserWithLeagues(BaseModel):
    user: User
    leagues: list[League]
