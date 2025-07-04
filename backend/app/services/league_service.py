from datetime import datetime

import httpx

from app.schemas import League


async def getLeague(league_id: str):
    URL = f"https://api.sleeper.app/v1/league/{league_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        league_data = response.json()

    league = League(
        id=league_data["league_id"],
        year=league_data["season"],
        previous_league_id=league_data["previous_league_id"],
        league_name=league_data["name"],
        last_week=league_data["settings"]["leg"],
    )
    return league


async def getLeaguesByYear(user_id: str, year: int):
    URL = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{year}"
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        leagues_data = response.json()

    leagues_list = []

    for league_data in leagues_data:
        league = League(
            id=league_data["league_id"],
            year=league_data["season"],
            previous_league_id=league_data["previous_league_id"],
            league_name=league_data["name"],
            last_week=league_data["settings"]["leg"],
        )
        leagues_list.append(league)

    return leagues_list


async def getRosterId(user_id: str, league_id: str):
    URL = f"https://api.sleeper.app/v1/league/{league_id}/rosters"

    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        league_data = response.json()

    for roster in league_data:
        if roster["owner_id"] == user_id:
            return roster["roster_id"]


async def createUserLeaguesList(user_id: str):
    current_year = datetime.now().year
    leagues_list_by_year = await getLeaguesByYear(user_id, current_year)
    unique_league_ids = []
    user_leagues = []

    group = 1
    year = 0

    while (current_year - year) >= 2015:
        for league in leagues_list_by_year:
            if league.id in unique_league_ids:
                continue
            unique_league_ids.append(league.id)
            roster_id = await getRosterId(user_id, league.id)

            league.roster_id = roster_id
            league.group_id = group
            user_leagues.append(league)

            previous_league_id = league.previous_league_id

            while previous_league_id not in (None, "0"):
                l = await getLeague(previous_league_id)

                if l.id in unique_league_ids:
                    previous_league_id = l.previous_league_id
                    continue
                unique_league_ids.append(l.id)

                roster_id = await getRosterId(user_id, l.id)
                l.roster_id = roster_id
                l.group_id = group

                user_leagues.append(l)

                previous_league_id = l.previous_league_id

            group += 1
        year += 1
        leagues_list_by_year = await getLeaguesByYear(user_id, current_year - year)
    return user_leagues
