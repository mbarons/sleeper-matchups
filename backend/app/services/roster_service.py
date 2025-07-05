import httpx
from sqlalchemy.orm import Session

from app.repositories import get_league_by_id
from app.schemas import League, Roster


async def getAllRosters(db: Session, leagues: list[League]) -> list[Roster] | None:
    ## de-para roster_id, owner_id por liga

    rosters: list[Roster] = []

    for league in leagues:

        # procurar league id
        existing_league = get_league_by_id(db, league.sleeper_league_id)

        # se eu já tiver essa liga no meu banco, significa que já tenho os rosters
        if existing_league is not None:
            continue

        URL = f"https://api.sleeper.app/v1/league/{league.sleeper_league_id}/rosters"

        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
            rosters_data = response.json()

        for r in rosters_data:
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
