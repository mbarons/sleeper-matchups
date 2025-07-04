from sqlalchemy.orm import Session

from app.models import RosterModel
from app.schemas import Roster


def save_rosters_to_db(rosters: list[Roster], db: Session):
    # adiciona em lote porque não precisamos conferir se já existe, e é mais performático
    roster_models = [RosterModel(**r.model_dump()) for r in rosters]
    db.add_all(roster_models)
    db.commit()


def get_all_rosters_from_db(db: Session) -> list[RosterModel]:
    rosters_db = db.query(RosterModel).all()
    return rosters_db
