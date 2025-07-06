from typing import Optional

from pydantic import BaseModel


class League(BaseModel):
    sleeper_league_id: str
    year: int
    league_name: str
    previous_league_id: Optional[str] = None
    last_week: int
    group_id: Optional[int] = None

    class Config:
        from_attributes = True
