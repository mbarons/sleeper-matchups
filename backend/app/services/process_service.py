import httpx
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.repositories import save_leagues_to_db, save_matches_to_db, save_rosters_to_db
from app.schemas import League, Matchup, Roster, User
from app.services.matchup_service import getAllMatchesFromLeague
from app.services.roster_service import getAllRosters
from app.services.user_service import get_all_users_from_league
from app.services.utils import medir_tempo_async, medir_tempo


@medir_tempo_async
async def process_filtered_leagues(user_id: str, leagues: list[League], db: Session):

    client = httpx.AsyncClient()

    # busca rosters e salva
    rosters: list[Roster] = await getAllRosters(db, leagues)
    save_rosters_to_db(rosters, db)

    # busca matches, users e salva
    matches: list[Matchup] = []
    users: list[User] = []
    for league in leagues:
        matches += await getAllMatchesFromLeague(league, client, db)
        users += await get_all_users_from_league(league, client, db)
    save_matches_to_db(db, matches)
    save_leagues_to_db(leagues, db)

    # remove usuários duplicados
    unique_users = list(set(users))

    # TODO não estamos salvando users
    result_df = process_result_df(user_id, unique_users, matches, rosters)
    # converter nan em none para conseguir usar o json
    result_df = result_df.where(pd.notnull(result_df), None)
    response = result_df.to_dict(orient="records")
    return response


@medir_tempo
def process_result_df(
    user_id: str, opponents: list[User], matches: list[Matchup], rosters: list[Roster]
):
    pd.set_option("display.max_columns", None)  # Mostra todas as colunas
    pd.set_option("display.width", None)  # Não quebra linha automaticamente
    pd.set_option(
        "display.max_colwidth", None
    )  # Mostra o conteúdo completo das colunas (se tiver texto grande)

    # transformamos listas em df
    matches_df = pd.DataFrame([m.model_dump() for m in matches])
    rosters_df = pd.DataFrame([r.model_dump() for r in rosters])
    opponents_df = pd.DataFrame([o.model_dump() for o in opponents])

    # juntamos os dois para termos as infos de user_id em matches
    matches_rosters = matches_df.merge(
        rosters_df, on=["sleeper_league_id", "roster_id"], how="left"
    )

    # filtramos somente as partidas do user
    user_matches = matches_rosters[matches_rosters["user_id"] == user_id]

    # procuramos os resultados dos oponentes e juntamos no df
    results = pd.merge(
        user_matches,
        matches_rosters,
        on=["sleeper_league_id", "matchup_id", "week"],
        suffixes=("_user", "_opp"),
    )

    # tiramos tudo que ficou com os dois users iguais (duplicamos na etapa anterior)
    results = results[results["user_id_user"] != results["user_id_opp"]]
    # renomeamos
    results = results[
        [
            "sleeper_league_id",
            "matchup_id",
            "week",
            "user_id_user",
            "points_user",
            "user_id_opp",
            "points_opp",
        ]
    ].rename(
        columns={
            "user_id_user": "user_id",
            "points_user": "user_points",
            "user_id_opp": "opp_id",
            "points_opp": "opp_points",
        }
    )
    # força pontos numéricos
    results["user_points"] = pd.to_numeric(results["user_points"], errors="coerce")
    results["opp_points"] = pd.to_numeric(results["opp_points"], errors="coerce")

    # Dropar linhas onde ambos os pontos são 0
    results = results[~((results["user_points"] == 0) & (results["opp_points"] == 0))]

    # Criar coluna "result" baseada na comparação dos pontos
    results["result"] = np.where(
        results["user_points"] > results["opp_points"],
        "W",
        np.where(results["user_points"] == results["opp_points"], "T", "L"),
    )

    # cria colunas numéricas para cada letra
    results["my_wins"] = (results["result"] == "W").astype(int)
    results["my_losses"] = (results["result"] == "L").astype(int)
    results["ties"] = (results["result"] == "T").astype(int)

    # agrega por oponente
    agg_df = (
        results.groupby("opp_id")[["my_wins", "my_losses", "ties"]].sum().reset_index()
    )
    agg_df["total_games"] = agg_df["my_wins"] + agg_df["my_losses"] + agg_df["ties"]

    agg_df.to_csv("agregado.csv")

    agg_merged_user = agg_df.merge(
        opponents_df, left_on="opp_id", right_on="user_id", how="left"
    ).sort_values(by="total_games", ascending=False)

    agg_merged_user.to_csv("agregado_com_dados.csv")
    return agg_merged_user
