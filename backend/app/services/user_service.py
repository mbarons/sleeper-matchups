import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import get_user_from_db
from app.schemas import User


async def getUser(username: str):
    URL = f"https://api.sleeper.app/v1/user/{username}"

    async with httpx.AsyncClient() as client:

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
async def get_all_users_from_league(list_ids: list[str], db: Session) -> list[User]:
    """
    Recebe uma lista de ids, e retorna uma lista de users.
    Busca no banco primeiro. Caso não tenha, busca na API.
    """

    users: list[User] = []

    for id in list_ids:
        user_db = get_user_from_db(id, db)

        if user_db:
            user = user_db.model_validate(user_db)
            users.append(user)
        else:
            user = await getUser(id)
            users.append(user)
    return users
