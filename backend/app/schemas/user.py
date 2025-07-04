from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    username: str
    display_name: str
    avatar: str

    class Config:
        from_attributes = True
