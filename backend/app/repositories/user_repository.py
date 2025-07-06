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


def get_all_users_from_db(db: Session):
    users_list = db.query(UserModel).all()
    return users_list
