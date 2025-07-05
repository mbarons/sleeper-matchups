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
