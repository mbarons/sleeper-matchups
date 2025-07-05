# main.py
"""Aplicação Streamlit simplificada"""

import api
import streamlit as st
import utils

# Interface do usuário
username = st.text_input("Sleeper username:")

if st.button("Send!"):

    # 1. Buscar usuário
    if not username:
        st.warning("Please insert an username.")
    else:
        user, error = api.get_user(username)

        if user:
            st.success("User found!")

            # 2. Buscar ligas
            user_id = user["user_id"]
            leagues, error = api.get_leagues(user_id)

            if leagues:
                st.success("Leagues found!")
                utils.show_dataframe(leagues, "Leagues")

                # 3. Buscar partidas
                matches, error = api.get_matches(leagues)
                if matches:
                    st.success("Matches found!")
                    utils.show_dataframe(matches, "Matches")
                else:
                    st.error(f"Erro ao buscar partidas! {error}")

                # 4. Buscar rosters
                rosters, error = api.get_rosters(leagues)
                if rosters:
                    st.success("Rosters found!")
                    utils.show_dataframe(rosters, "Rosters")
                else:
                    st.error(f"Erro ao buscar rosters! {error}")

                # 5. Salvar ligas no banco
                success, error = api.save_leagues(leagues)
                if success:
                    st.success("Leagues saved to database!")
                else:
                    st.error(f"Erro ao salvar ligas! {error}")

                # 6. Processamento opcional das ligas (descomente se quiser usar)
                # df = utils.process_leagues_dataframe(leagues)
                # league_names = utils.get_league_names(df)
                # st.selectbox("Selecione as ligas", league_names)
                # st.dataframe(df)

            else:
                st.error(f"Erro ao buscar ligas! {error}")
        else:
            st.error(f"Erro ao buscar usuário! {error}")
