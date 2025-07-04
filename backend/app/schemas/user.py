from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    display_name: str
    avatar: str
    leagues: List = []
    matchups: List = []  ## verificar necessidade

    class Config:
        from_attributes = True
