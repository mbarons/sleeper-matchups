import httpx

from app.schemas import League, Roster
from app.repositories import get_league_by_id
from app.database import get_db
from sqlalchemy.orm import Session


async def getRosterId(user_id: str, league_id: str):
    URL = f"https://api.sleeper.app/v1/league/{league_id}/rosters"

    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        league_data = response.json()

    for roster in league_data:
        if roster["owner_id"] == user_id:
            return roster["roster_id"]


async def getAllRosterId(db: Session, leagues: list[League]):
    ## de-para roster_id, owner_id por liga

    rosters = []

    for league in leagues:

        # procurar league id
        existing_league = get_league_by_id(db, league.id)

        if existing_league is not None:
            continue

        URL = f"https://api.sleeper.app/v1/league/{league.id}/rosters"

        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
            rosters_data = response.json()

        for r in rosters_data:
            roster = Roster(
                user_id=r["owner_id"], league_id=league.id, roster_id=r["roster_id"]
            )
            rosters.append(roster)
    return rosters
