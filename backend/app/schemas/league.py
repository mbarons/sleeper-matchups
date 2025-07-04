from typing import Optional

from pydantic import BaseModel


class League(BaseModel):
    id: str
    year: int
    league_name: str
    previous_league_id: Optional[str] = None
    last_week: int
    group_id: Optional[int] = None
    roster_id: Optional[int] = None

    class Config:
        from_attributes = True
