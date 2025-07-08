import api
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
        response, error = api.get_leagues(username)

        if response:
            user = response["user"]
            leagues = response["leagues"]

            st.session_state["user"] = user
            st.session_state["user_id"] = user["user_id"]
            st.session_state["leagues"] = leagues

        else:
            st.error(f"Erro ao buscar dados! {error}")

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

    if filtered_leagues:
        if st.button("Run!"):
            response, error = api.process_results(
                st.session_state["user_id"], filtered_leagues
            )

            if error:
                st.error(f"Erro: {error}")
            elif response:
                for line in response:
                    st.write(
                        f"{st.session_state['user']['username']} | {line['my_wins']} | - | {line['my_losses']} | {line['username']}"
                    )

            else:
                st.error("Erro na resposta da API.")
