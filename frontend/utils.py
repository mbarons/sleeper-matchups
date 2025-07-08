# utils.py
"""Funções auxiliares"""

import numpy as np
import pandas as pd
import streamlit as st


def show_dataframe(data, title):
    """Exibe DataFrame no Streamlit"""
    if data:
        st.subheader(title)
        df = pd.DataFrame(data)
        st.dataframe(df)


def keep_lastest_league_in_group(leagues: list[dict]):
    """
    recebe uma lista de ligas com groupid, e retorna uma lista com apenas as ligas de maior ano por groupid
    """
    best_by_groupid = {}

    for league in leagues:
        group_id = league["group_id"]

        if (
            group_id not in best_by_groupid
            or league["year"] > best_by_groupid[group_id]["year"]
        ):
            best_by_groupid[group_id] = league

    return list(best_by_groupid.values())


def get_league_names(df):
    """Extrai nomes das ligas do DataFrame processado"""
    return (
        df.loc[df.groupby("group_id")["year"].idxmax()]
        .sort_values("group_id")["league_name"]
        .tolist()
    )


def get_results(user_id: str, matches_df: pd.DataFrame):
    """
    Cria o df junta as partidas entre os dois jogadores, e define o vencedor
    """
    user_matches = matches_df[matches_df["user_id"] == user_id]

    results = pd.merge(
        user_matches,
        matches_df,
        on=["sleeper_league_id", "matchup_id", "week"],
        suffixes=("_user", "_opp"),
    )

    results = results[results["user_id_user"] != results["user_id_opp"]]

    results_final = results[
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
    results_final["user_points"] = pd.to_numeric(
        results_final["user_points"], errors="coerce"
    )
    results_final["opp_points"] = pd.to_numeric(
        results_final["opp_points"], errors="coerce"
    )

    # Dropar linhas onde ambos os pontos são 0
    results_final = results_final[
        ~((results_final["user_points"] == 0) & (results_final["opp_points"] == 0))
    ]

    # Criar coluna "result" baseada na comparação dos pontos
    results_final["result"] = np.where(
        results_final["user_points"] > results_final["opp_points"],
        "W",
        np.where(results_final["user_points"] == results_final["opp_points"], "T", "L"),
    )

    return results_final
