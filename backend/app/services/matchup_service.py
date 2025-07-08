import httpx
from sqlalchemy.orm import Session

from app.repositories import get_league_last_played_week, get_matches_from_league
from app.schemas import League, Matchup
from app.services.utils import medir_tempo_async


@medir_tempo_async
async def getMatchupWeek(
    league: League, week: int, client: httpx.AsyncClient
) -> list[Matchup] | None:

    URL = (
        f"https://api.sleeper.app/v1/league/{league.sleeper_league_id}/matchups/{week}"
    )

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


@medir_tempo_async
async def getAllMatchesFromLeague(
    league: League, client: httpx.AsyncClient, db: Session
) -> list[Matchup]:

    # busca a last_week da liga no db (liga não existe retorna 0)
    last_played_week = get_league_last_played_week(league.sleeper_league_id, db)

    matches: list[Matchup] = []
    # pegamos as partidas do db (is_new=false)
    matches += get_matches_from_league(league.sleeper_league_id, db)

    # se last week do db for diferente da api, significa que não temos todas as semanas
    # precisamos iterar a partir daquela semana
    # caso não tenha a liga, a função vai retornar 0, e pegaremos todos as semanas.

    i = last_played_week + 1

    for w in range(i, league.last_week + 1):
        week = await getMatchupWeek(league, w, client)

        if week is None:
            continue

        for m in week:
            matches.append(m)

    return matches
