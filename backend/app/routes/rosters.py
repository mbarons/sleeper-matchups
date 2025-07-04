from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import get_db
from app.repositories import get_all_rosters_from_db
from app.schemas import Roster

router = APIRouter(prefix="/rosters", tags=["rosters"])


@router.get("/", response_model=list[Roster])
async def get_all_rosters(db: Session = Depends(get_db)):
    rosters_db = get_all_rosters_from_db(db)
    rosters = [Roster.model_validate(roster) for roster in rosters_db]
    return rosters
