from app.schemas import Roster
from sqlalchemy.orm import Session
from app.models import RosterModel, LeagueModel


def save_rosters_to_db(rosters: list[Roster], db: Session):
    for roster in rosters:
        # Verifica se já existe
        db_league = db.query(LeagueModel).filter(LeagueModel.sleeper_id==roster.league_id).first()
        if db_league:
            db_league_id = db_league.db_id
            db_roster = db.query(RosterModel).filter(RosterModel.db_league_id==db_league_id)
            
            if db_roster:
                continue
        
            ####continuar aqui
        league_db = LeagueModel(
            **{**league.model_dump(exclude={"id"}), "sleeper_id": league.id},
            user_id=user_id,
        )
        db.add(league_db)
    db.commit()
