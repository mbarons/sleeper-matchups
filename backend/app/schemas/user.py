from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    username: str
    display_name: str
    avatar: Optional[str]
    is_new: bool = True

    class Config:
        from_attributes = True
        frozen = True  # permite usar sets (para verificar duplicados)
