from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_name = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())


class LeagueModel(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sleeper_league_id = Column(String)
    previous_league_id = Column(String)
    year = Column(Integer)
    league_name = Column(String)
    last_week = Column(Integer)
    group_id = Column(Integer)


class RosterModel(Base):
    __tablename__ = "rosters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    db_league_id = Column(Integer, ForeignKey("leagues.id"))
    roster_id = Column(Integer)
