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


def get_matches_from_league(league_id: str, db: Session) -> list[Matchup]:
    matches_db = (
        db.query(MatchupModel).filter(MatchupModel.sleeper_league_id == league_id).all()
    )

    matches = [Matchup.model_validate(match) for match in matches_db]
    return matches


def save_matches_to_db(db: Session, matches: list[Matchup]):
    for match in matches:

        # TODO: se um usuário consultou em 2024 no meio de uma partida, vamos pegar um resultado parcial e salvar
        # caso ele faça uma nova consulta em 2025, esse resultado parcial não será atualizado...
        # além disso, resultados parciais serão contabilizados

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
            match_db = MatchupModel(**match.model_dump())
            db.add(match_db)
    db.commit()
