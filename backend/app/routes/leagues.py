from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import get_db
from app.repositories import (
    get_all_leagues_from_db,
    save_leagues_to_db,
)
from app.schemas import League
from app.services import (
    createUserLeaguesList,
)

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("/{user_id}", response_model=list[League])
async def get_leagues_from_user(user_id: str):

    # TODO: entender o que acontece se não tiver ligas
    try:
        leagues = await createUserLeaguesList(user_id)
        return leagues

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar ligas: {e}")


@router.get("/", response_model=list[League])
async def get_all_leagues(db: Session = Depends(get_db)):
    leagues_db = get_all_leagues_from_db(db)
    leagues = [League.model_validate(user) for user in leagues_db]
    return leagues


@router.post("/")
async def save_leagues(leagues: list[League], db: Session = Depends(get_db)):
    save_leagues_to_db(leagues, db)
