from sqlalchemy.orm import Session

from app.models import LeagueModel
from app.schemas import League


def save_leagues_to_db(leagues: list[League], db: Session):
    for league in leagues:
        # Verifica se já existe
        existing = (
            db.query(LeagueModel)
            .filter(LeagueModel.sleeper_id == league.sleeper_league_id)
            .first()
        )
        if existing:
            continue  # já existe, pula
        league_db = LeagueModel(**league.model_dump())
        db.add(league_db)
    db.commit()


def get_league_by_id(db: Session, sleeper__league_id: str) -> LeagueModel | None:
    return db.query(LeagueModel).filter(LeagueModel.sleeper_league_id == sleeper__league_id).first()
