from datetime import datetime

import httpx

from app.schemas import League
from app.services.utils import medir_tempo, medir_tempo_async


@medir_tempo_async
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
            last_week=league_data.get("settings", {}).get("last_scored_leg", 0),
        )

        if league.last_week == 0:
            continue

        leagues_list.append(league)

    return leagues_list


@medir_tempo_async
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

    leagues_with_group_id = process_leagues_groupid(user_leagues)

    return leagues_with_group_id


@medir_tempo
def process_leagues_groupid(leagues: list[League]):
    """essa função recebe uma lista de ligas sem group ids e devolve a lista com group ids"""

    sorted_leagues = sorted(leagues, key=lambda x: x.year, reverse=True)

    visiteds: list[League] = []
    group_id = 0

    for league in reversed(sorted_leagues):
        for previous in visiteds:
            if league.previous_league_id == previous.sleeper_league_id:
                league.group_id = previous.group_id
                visiteds.append(league)
                break
        else:  # esse else é do for... só executa se o for não encontrar o break.
            group_id += 1
            league.group_id = group_id
            visiteds.append(league)

    return sorted_leagues
