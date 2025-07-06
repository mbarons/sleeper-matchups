import httpx
from fastapi import HTTPException

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
