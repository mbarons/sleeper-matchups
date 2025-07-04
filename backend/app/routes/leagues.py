from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import get_db
from app.models import LeagueModel
from app.repositories import save_leagues_to_db
from app.schemas import League
from app.services import createUserLeaguesList, getUser

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("/{user_name}", response_model=list[League])
async def get_leagues(user_name: str, db: Session = Depends(get_db)):

    try:
        user = await getUser(user_name)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados externos: {e}"
        )

    existing_leagues = db.query(LeagueModel).filter_by(user_id=user.id).all()

    if existing_leagues:
        leagues = [League.model_validate(league) for league in existing_leagues]
        return leagues

    try:
        leagues = await createUserLeaguesList(user.id)
        save_leagues_to_db(user.id, leagues, db)
        return leagues
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados externos: {e}"
        )
