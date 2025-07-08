from typing import Optional

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import get_user_from_db
from app.schemas import League, User
from app.services.utils import medir_tempo_async


@medir_tempo_async
async def getUser(
    client: httpx.AsyncClient,
    db: Session,
    username: Optional[str] = None,
    user_id: Optional[str] = None,
) -> User:

    if not username and not user_id:
        raise ValueError("You must provide username or user id.")

    user = get_user_from_db(db, user_id=user_id, username=username)

    # TODO se ele já existir no db não iremos atualizar display name e avatar
    if user:
        return user
    if username:
        URL = f"https://api.sleeper.app/v1/user/{username}"
    else:
        URL = f"https://api.sleeper.app/v1/user/{user_id}"

    response = await client.get(URL)
    user_data = response.json()

    if user_data is None:
        raise HTTPException(
            status_code=404,
            detail=f'User: "{username}" not found in sleeper database.',
        )

    user = User(
        user_id=user_data["user_id"],
        username=user_data["username"],
        display_name=user_data["display_name"],
        avatar=user_data["avatar"],
    )

    return user


# TODO criar função para armazenar usuários de oponentes
@medir_tempo_async
async def get_all_users_from_league(
    league: League, client: httpx.AsyncClient, db: Session
) -> list[User]:
    """
    Recebe uma liga e retorna uma lista de users.
    Busca no banco primeiro. Caso não tenha, busca na API.
    """

    URL = f"https://api.sleeper.app/v1/league/{league.sleeper_league_id}/users"

    response = await client.get(URL)
    users_data = response.json()

    ids: list[str] = []

    for u in users_data:
        ids.append(u["user_id"])

    users: list[User] = []

    for id in ids:
        user = await getUser(client, db, user_id=id)
        users.append(user)

    return users
