from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import get_db
from app.repositories import get_all_users_from_db, save_user_to_db
from app.schemas import User
from app.services import getUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
async def get_all_users(db: Session = Depends(get_db)):
    users_db = get_all_users_from_db(db)
    users = [User.model_validate(user) for user in users_db]
    return users


@router.post("/{username}", response_model=User)
async def get_user_from_sleeper(username: str, db: Session = Depends(get_db)):

    # TODO:implementar lógica caso o usuário ja existir

    try:
        user: User = await getUser(username)
        save_user_to_db(user, db)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar usuário: {e}")
