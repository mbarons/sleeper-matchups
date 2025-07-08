from typing import Optional

from sqlalchemy.orm import Session

from app.models import UserModel
from app.schemas import User


def save_user_to_db(user: User, db: Session):

    existing = db.query(UserModel).filter(UserModel.user_id == user.user_id).first()

    if existing:
        return

    user_db = UserModel(**user.model_dump())
    db.add(user_db)
    db.commit()


def get_all_users_from_db(db: Session) -> list[UserModel]:
    users_list = db.query(UserModel).all()
    return users_list


def get_user_from_db(
    db: Session, user_id: Optional[str] = None, username: Optional[str] = None
) -> User | None:

    if not user_id and not username:
        raise ValueError("You must provide user_id or username")

    user_db: UserModel | None = None

    if user_id:
        user_db = db.query(UserModel).filter(UserModel.user_id == user_id).first()

    elif username:
        user_db = db.query(UserModel).filter(UserModel.username == username).first()

    if not user_db:
        return None

    user = User.model_validate(user_db)
    user.is_new = False

    return user
