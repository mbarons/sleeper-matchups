import httpx
from schemas import League, Matchup


async def getMatchupWeek(league_id: str, week: int) -> list[Matchup] | None:

    URL = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        matchup_data = response.json()

    matches = []

    for m in matchup_data:
        match = Matchup(
            matchup_id=m["matchup_id"],
            sleeper_league_id=league_id,
            points=m["points"],
            week=week,
        )
        matches.append(match)
    return matches


def getMatchupId(week_data, roster_id: int):
    for match in week_data:
        if match["roster_id"] == roster_id:
            return match["matchup_id"]


def getOpponent(week_data, matchup_id: int, roster_id: int):
    for match in week_data:
        if match["matchup_id"] == matchup_id and match["roster_id"] != roster_id:
            return match["roster_id"]


def getPoints(week_data, roster_id: int):
    for match in week_data:
        if match["roster_id"] == roster_id:
            return match["points"]


def getOppUserId(roster_id: int, league_id: str):
    for roster in rosters:
        if roster[0] == league_id and roster[2] == roster_id:
            return roster[1]


def defineMatchup(week_data, week: int, league: League):
    # achar meu matchup_id com base no meu roster id
    matchup_id = findMatchupId(week_data, league.roster_id)
    print(f"matchup: {matchup_id}")

    if matchup_id is None:
        return None
