from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import save_matches_to_db
from app.schemas import League, Matchup
from app.services import getAllMatchesFromLeague

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("/", response_model=list[Matchup])
async def get_matches(leagues: list[League], db: Session = Depends(get_db)):
    if leagues:
        matches_list = []
        for league in leagues:
            matches = await getAllMatchesFromLeague(league, db)
            if matches:
                matches_list.extend(matches)
        save_matches_to_db(db, matches_list)
        return matches_list
