from sqlalchemy.orm import Session

from app.models import MatchupModel
from app.schemas import Matchup


def get_matches_from_league(league_id: str, db: Session) -> list[Matchup]:
    matches_db = (
        db.query(MatchupModel).filter(MatchupModel.sleeper_league_id == league_id).all()
    )

    matches = [Matchup.model_validate(match) for match in matches_db]
    for match in matches:
        match.is_new = False
    return matches


def save_matches_to_db(db: Session, matches: list[Matchup]):
    for match in matches:

        # caso seja desse ano, verificamos se ela está no db
        existing = (
            db.query(MatchupModel)
            .filter(
                MatchupModel.sleeper_league_id == match.sleeper_league_id,
                MatchupModel.year == match.year,
                MatchupModel.week == match.week,
            )
            .first()
        )
        if not existing:
            match_db = MatchupModel(**match.model_dump(exclude={"is_new"}))
            db.add(match_db)
    db.commit()
