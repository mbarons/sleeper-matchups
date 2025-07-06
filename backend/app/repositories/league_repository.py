from sqlalchemy.orm import Session

from app.models import LeagueModel
from app.schemas import League


def save_leagues_to_db(leagues: list[League], db: Session):
    for league in leagues:
        # Verifica se já existe
        existing = (
            db.query(LeagueModel)
            .filter(LeagueModel.sleeper_league_id == league.sleeper_league_id)
            .first()
        )
        if existing:
            continue  # já existe, pula
        league_db = LeagueModel(**league.model_dump(exclude={"group_id"}))
        db.add(league_db)
    db.commit()


def get_league_by_id(db: Session, sleeper__league_id: str) -> LeagueModel | None:
    return (
        db.query(LeagueModel)
        .filter(LeagueModel.sleeper_league_id == sleeper__league_id)
        .first()
    )


def get_all_leagues_from_db(db: Session) -> list[LeagueModel]:
    leagues_list = db.query(LeagueModel).all()
    return leagues_list


def get_league_last_played_week(league_id: str, db: Session) -> int:
    league_db = (
        db.query(LeagueModel).filter(LeagueModel.sleeper_league_id == league_id).first()
    )

    if league_db:
        return league_db.last_week  # type: ignore (pylance lance não entende que é int)
    else:
        return 0
