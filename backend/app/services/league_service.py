from datetime import datetime

import httpx

from app.schemas import League


async def getLeague(league_id: str):
    URL = f"https://api.sleeper.app/v1/league/{league_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        league_data = response.json()

    league = League(
        sleeper_league_id=league_data["league_id"],
        year=league_data["season"],
        previous_league_id=league_data["previous_league_id"],
        league_name=league_data["name"],
        last_week=league_data["settings"]["leg"],
    )
    return league


async def getLeaguesByYear(user_id: str, year: int) -> list[League]:
    URL = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{year}"
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        leagues_data = response.json()

    leagues_list = []

    for league_data in leagues_data:
        league = League(
            sleeper_league_id=league_data["league_id"],
            year=league_data["season"],
            previous_league_id=league_data["previous_league_id"],
            league_name=league_data["name"],
            last_week=league_data["settings"]["leg"],
        )
        leagues_list.append(league)

    return leagues_list


async def createUserLeaguesList(user_id: str) -> list[League]:
    current_year = datetime.now().year
    leagues_list_by_year = await getLeaguesByYear(user_id, current_year)
    user_leagues = []

    year = 0

    while (current_year - year) >= 2015:

        if leagues_list_by_year is None:
            year += 1
            pass

        for league in leagues_list_by_year:
            user_leagues.append(league)
        year += 1
        leagues_list_by_year = await getLeaguesByYear(user_id, current_year - year)
    return user_leagues
