import api
import pandas as pd
import streamlit as st
import utils

# Interface do usuário
username = st.text_input("Sleeper username:")

# botão de envio

user = {}

if st.button("Send!"):
    if not username:
        st.warning("Please insert an username.")
    else:
        user, error = api.get_user(username)

        if user:
            st.session_state["user"] = user
            st.session_state["user_id"] = user["user_id"]

            leagues, error = api.get_leagues(user["user_id"])
            if leagues:
                st.session_state["leagues"] = leagues
                st.success("Leagues loaded!")
            else:
                st.error(f"Erro ao buscar ligas! {error}")
        else:
            st.error(f"Erro ao buscar usuário! {error}")

# Após carregamento bem-sucedido
if "leagues" in st.session_state:
    leagues = st.session_state["leagues"]
    league_groups = utils.keep_lastest_league_in_group(leagues)

    # Multiselect com nomes das ligas
    selected_league_names = st.multiselect(
        "Choose your leagues:",
        options=[g["league_name"] for g in league_groups],
    )

    # busca os grupos das ligas selecionadas
    selected_group_ids = [
        g["group_id"]
        for g in league_groups
        if g["league_name"] in selected_league_names
    ]

    # busca os anos dos grupos selecionados
    available_years = sorted(
        list({l["year"] for l in leagues if l["group_id"] in selected_group_ids}),
        reverse=True,
    )

    selected_years = st.pills(
        "Select available years:",
        options=available_years,
        format_func=str,
        selection_mode="multi",
    )

    filtered_leagues = [
        l
        for l in leagues
        if l["group_id"] in selected_group_ids and l["year"] in selected_years
    ]

    utils.show_dataframe(filtered_leagues, "Ligas filtradas")

    matches, rosters = [], []

    if st.button("Run!"):
        if filtered_leagues:
            # busca matches e salva no db

            matches, error = api.get_matches(filtered_leagues)
            if matches:
                st.success("Matches found!")
            else:
                st.error(f"Erro ao buscar partidas! {error}")

            # busca rosters e salva no db
            rosters, error = api.get_rosters(filtered_leagues)
            if rosters:
                st.success("Rosters found!")
            else:
                st.error(f"Erro ao buscar rosters! {error}")

            # buscar users e salva no db

            # salva ligas no db
            success, error = api.save_leagues(filtered_leagues)
            if success:
                st.success("Leagues saved to database!")
            else:
                st.error(f"Erro ao salvar ligas! {error}")

        user = st.session_state["user"]
        if matches and rosters and user:
            matches_df = pd.DataFrame(matches)
            rosters_df = pd.DataFrame(rosters)

            matches_rosters = matches_df.merge(
                rosters_df, on=["sleeper_league_id", "roster_id"], how="left"
            )

            df_results = utils.get_results(user["user_id"], matches_rosters)
            df_final = utils.get_final_df(df_results)
            st.dataframe(df_final)
