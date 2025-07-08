from sqlalchemy.orm import Session

from app.models import RosterModel
from app.schemas import Roster


def save_rosters_to_db(rosters: list[Roster], db: Session):
    # só adiciona se for new
    for r in rosters:
        if r.is_new:
            r_db = RosterModel(**r.model_dump(exclude={"is_new"}))
            db.add(r_db)
    db.commit()


def get_all_rosters_from_db(db: Session) -> list[RosterModel]:
    rosters_db = db.query(RosterModel).all()
    return rosters_db


def get_rosters_from_league(league_id: str, db: Session) -> list[Roster]:
    rosters_db = (
        db.query(RosterModel).filter(RosterModel.sleeper_league_id == league_id).all()
    )

    rosters = [Roster.model_validate(roster) for roster in rosters_db]
    for r in rosters:
        r.is_new = False
    return rosters
