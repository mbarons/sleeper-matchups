# utils.py
"""Funções auxiliares"""

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


def process_leagues_dataframe(leagues_data):
    """Processa dados das ligas e cria DataFrame com group_id"""
    df = pd.DataFrame(leagues_data)

    processed = {}
    current_group_id = 1

    for idx in reversed(df.index):
        row = df.loc[idx]
        league_id = row["sleeper_league_id"]
        prev_id = row["previous_league_id"]

        if idx == df.index[-1]:
            # Primeira linha da iteração (última do df)
            df.at[idx, "group_id"] = current_group_id
            processed[league_id] = current_group_id
        else:
            if prev_id in processed:
                # copia o group_id do previous_league_id
                df.at[idx, "group_id"] = processed[prev_id]
                processed[league_id] = processed[prev_id]
            else:
                # novo group_id incremental
                current_group_id += 1
                df.at[idx, "group_id"] = current_group_id
                processed[league_id] = current_group_id

    return df


def get_league_names(df):
    """Extrai nomes das ligas do DataFrame processado"""
    return (
        df.loc[df.groupby("group_id")["year"].idxmax()]
        .sort_values("group_id")["league_name"]
        .tolist()
    )


def get_results(user_id: str, matches_df: pd.DataFrame):
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

    return results_final
