from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import get_db
from app.repositories import (
    get_all_leagues_from_db,
    save_leagues_to_db,
    save_matches_to_db,
    save_rosters_to_db,
    save_user_to_db,
)
from app.schemas import League, User
from app.services import (
    createUserLeaguesList,
    getAllMatchesFromLeague,
    getAllRosters,
    getUser,
)

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("/{username}", response_model=list[League])
async def get_leagues(username: str, db: Session = Depends(get_db)):

    try:
        user: User = await getUser(username)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados externos: {e}"
        )

    save_user_to_db(user, db)

    try:
        leagues = await createUserLeaguesList(user.user_id)
        matches_list = []
        rosters = []

        if leagues:
            for league in leagues:
                matches = await getAllMatchesFromLeague(league, db)
                if matches:
                    matches_list.extend(matches)

        # rosters deve buscar primeiro, pq ele vai conferir se as ligas estão no banco,
        # se salvar as ligas primeiro, não vai buscar.
        if leagues:
            rosters = await getAllRosters(db, leagues)
            save_leagues_to_db(leagues, db)

        if rosters:
            save_rosters_to_db(rosters, db)
        if matches_list:
            print(matches_list)
            save_matches_to_db(db, matches_list)

        return leagues
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados externos: {e}"
        )


@router.get("/", response_model=list[League])
async def get_all_leagues(db: Session = Depends(get_db)):
    leagues_db = get_all_leagues_from_db(db)
    leagues = [League.model_validate(user) for user in leagues_db]
    return leagues
