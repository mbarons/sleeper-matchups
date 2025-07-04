from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import get_db
from app.repositories import get_all_users_from_db
from app.schemas import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
async def get_all_users(db: Session = Depends(get_db)):
    users_db = get_all_users_from_db(db)
    users = [User.model_validate(user) for user in users_db]
    return users
