from pydantic import BaseModel


class Matchup(BaseModel):
    matchup_id: int
    league_id: str
    opp_id: str
    result: str
    year: int
    week: int

    class Config:
        from_attributes = True
