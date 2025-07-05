from datetime import datetime

from sqlalchemy.orm import Session

from app.models import MatchupModel
from app.schemas import Matchup


def does_league_exists_in_matches(league_id: str, db: Session) -> bool:
    return (
        db.query(MatchupModel)
        .filter(MatchupModel.sleeper_league_id == league_id)
        .first()
        is not None
    )


def save_matches_to_db(db: Session, matches: list[Matchup]):
    for match in matches:

        # se a partida não for desse ano, adicionamos (já sabemos que não está no db)
        if match.year != datetime.now().year:
            match_db = MatchupModel(**match.model_dump())
            db.add(match_db)
            continue

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
        # se estiver atualizamos
        if existing:
            for key, value in match.model_dump().items():
                setattr(existing, key, value)
        # se não, inserimos
        else:
            match_db = MatchupModel(**match.model_dump())
            db.add(match_db)
    db.commit()
