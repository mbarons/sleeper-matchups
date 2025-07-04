import httpx
from sqlalchemy.orm import Session

from app.repositories import get_league_by_id
from app.schemas import League, Roster


async def getRosterId(user_id: str, league_id: str):
    URL = f"https://api.sleeper.app/v1/league/{league_id}/rosters"

    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        league_data = response.json()

    for roster in league_data:
        if roster["owner_id"] == user_id:
            return roster["roster_id"]


async def getAllRosters(db: Session, leagues: list[League]):
    ## de-para roster_id, owner_id por liga

    rosters: list[Roster] = []

    for league in leagues:

        # procurar league id
        existing_league = get_league_by_id(db, league.sleeper_league_id)

        if existing_league is not None:
            continue

        URL = f"https://api.sleeper.app/v1/league/{league.sleeper_league_id}/rosters"

        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
            rosters_data = response.json()

        for r in rosters_data:
            print(r["owner_id"])
            # caso tenha um roster sem user_id - pode acontecer se alguém saiu da liga
            if r["owner_id"] is None:
                roster = Roster(
                    user_id="NotFound",
                    sleeper_league_id=league.sleeper_league_id,
                    roster_id=r["roster_id"],
                )
                rosters.append(roster)
                continue

            roster = Roster(
                user_id=r["owner_id"],
                sleeper_league_id=league.sleeper_league_id,
                roster_id=r["roster_id"],
            )
            rosters.append(roster)
    return rosters
