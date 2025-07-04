from pydantic import BaseModel
from decimal import Decimal


class Matchup(BaseModel):
    matchup_id: int
    sleeper_league_id: str
    points: Decimal
    week: int

    class Config:
        from_attributes = True
