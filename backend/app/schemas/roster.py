from pydantic import BaseModel


class Roster(BaseModel):
    user_id: str
    sleeper_league_id: str
    roster_id: int

    class Config:
        from_attributes = True
