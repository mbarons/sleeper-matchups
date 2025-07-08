from decimal import Decimal

from pydantic import BaseModel


class Matchup(BaseModel):
    matchup_id: int
    sleeper_league_id: str
    roster_id: int
    points: Decimal
    year: int
    week: int
    is_new: bool = True

    class Config:
        from_attributes = True
