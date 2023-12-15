from typing import List
from elo_rank import db
from sqlalchemy import Boolean, Column, DateTime, Integer, ForeignKey


class Match(db.Model):
    __tablename__ = "matches"

    id = Column("match_id", Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    player_a_id = Column(Integer, ForeignKey("users.user_id"))
    player_b_id = Column(Integer, ForeignKey("users.user_id"))
    set_1 = Column(Integer, nullable=False)
    set_2 = Column(Integer, nullable=False)
    set_3 = Column(Integer)
    player_a_won = Column(Boolean)
