from sqlalchemy.orm import Session

from app.models import LeagueModel
from app.schemas import League


def save_leagues_to_db(user_id: str, leagues: list[League], db: Session):
    for league in leagues:
        # Verifica se já existe
        existing = db.query(LeagueModel).filter_by(sleeper_id=league.id).first()
        if existing:
            continue  # já existe, pula
        league_db = LeagueModel(
            **{**league.model_dump(exclude={"id"}), "sleeper_id": league.id},
            user_id=user_id,
        )
        db.add(league_db)
    db.commit()
