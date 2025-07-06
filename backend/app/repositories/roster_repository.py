from sqlalchemy.orm import Session

from app.models import RosterModel
from app.schemas import Roster


def save_rosters_to_db(rosters: list[Roster], db: Session):
    for r in rosters:
        exists = (
            db.query(RosterModel)
            .filter_by(sleeper_league_id=r.sleeper_league_id, roster_id=r.roster_id)
            .first()
        )

        if not exists:
            new_roster = RosterModel(**r.model_dump())
            db.add(new_roster)

    db.commit()


def get_all_rosters_from_db(db: Session) -> list[RosterModel]:
    rosters_db = db.query(RosterModel).all()
    return rosters_db


def get_rosters_from_league(league_id: str, db: Session) -> list[Roster]:
    rosters_db = (
        db.query(RosterModel).filter(RosterModel.sleeper_league_id == league_id).all()
    )

    rosters = [Roster.model_validate(roster) for roster in rosters_db]
    return rosters
