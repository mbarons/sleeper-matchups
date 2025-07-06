import httpx
from sqlalchemy.orm import Session

from app.repositories import does_league_exists_in_matches, get_matches_from_league
from app.schemas import League, Matchup


async def getMatchupWeek(league: League, week: int) -> list[Matchup] | None:

    URL = (
        f"https://api.sleeper.app/v1/league/{league.sleeper_league_id}/matchups/{week}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        matchup_data = response.json()

    matches = []

    for m in matchup_data:

        if m["matchup_id"] is None:
            continue

        match = Matchup(
            matchup_id=m["matchup_id"],
            sleeper_league_id=league.sleeper_league_id,
            roster_id=m["roster_id"],
            points=m["points"],
            year=league.year,
            week=week,
        )
        matches.append(match)
    return matches


async def getAllMatchesFromLeague(league: League, db: Session) -> list[Matchup] | None:

    # se já existir, pega do db
    exist = does_league_exists_in_matches(league.sleeper_league_id, db)

    if exist:
        return get_matches_from_league(league.sleeper_league_id, db)

    matches = []

    for w in range(1, league.last_week + 1):
        week = await getMatchupWeek(league, w)

        if week is None:
            continue

        for m in week:
            matches.append(m)

    return matches
