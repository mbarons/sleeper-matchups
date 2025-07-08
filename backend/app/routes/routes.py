import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import League, User, UserWithLeagues
from app.services import (
    createUserLeaguesList,
    getUser,
    process_filtered_leagues,
    process_leagues_groupid,
)

router = APIRouter()


# TODO verificar se liga já existe no db (checar semana tbm é importante)
@router.get("/leagues/{user_name}", response_model=UserWithLeagues)
async def get_leagues_for_user(user_name: str, db: Session = Depends(get_db)):
    client = httpx.AsyncClient()
    try:
        user: User = await getUser(client, db, username=user_name)
        leagues: list[League] = await createUserLeaguesList(user.user_id)

    except HTTPException:
        raise
    except Exception:
        raise (
            HTTPException(
                status_code=500,
                detail="Something went wrong fetching data (users/leagues) from sleeper.",
            )
        )

    leagues_with_groups = process_leagues_groupid(leagues)
    user_with_leagues = UserWithLeagues(user=user, leagues=leagues_with_groups)
    return user_with_leagues


@router.post("/leagues/process/{user_id}")
async def process_results(
    request: list[League], user_id: str, db: Session = Depends(get_db)
):
    try:
        response = await process_filtered_leagues(user_id, request, db)
        return response
    except Exception:
        raise
