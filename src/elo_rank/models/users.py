from __future__ import annotations
from typing import Optional
from elo_rank import db
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
import datetime as dt
from flask_login import UserMixin
from elo_rank.lib import compute_elo_movement
from .matches import Match


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    score = Column(Integer, nullable=False, default=500)
    score_computed_at = Column(DateTime)

    def report_match(
        self,
        player_b: User,
        set_1: int,
        set_2: int,
        set_3: Optional[int] = None,
    ):
        if any([s == 0 for s in [set_1, set_2]]):
            raise ValueError(f"Cannot submit a set score of 0.")

        set_3_points = 0 if set_3 is None else set_3
        sets = [set_1, set_2, set_3_points]
        sets_won_by_player_a = [1 if s > 0 else 0 for s in sets]

        sets_won_by_player_b = [0 if s > 0 else 1 for s in sets]
        if sets_won_by_player_a == sets_won_by_player_b:
            raise ValueError(f"The players cannot submit a draw.")

        player_a_won = sum(sets_won_by_player_a) >= 2
        new_match = Match(
            date=dt.datetime.now(),
            player_a_id=self.get_id(),
            player_b_id=player_b.get_id(),
            set_1=set_1,
            set_2=set_2,
            set_3=set_3,
            player_a_won=player_a_won,
        )

        match_history_player_a = UserMatchHistory(
            player_id=self.get_id(),
            opponent_id=player_b.get_id(),
            elo_movement=compute_elo_movement(self.score, player_b.score, player_a_won),
        )
        match_history_player_b = UserMatchHistory(
            player_id=player_b.get_id(),
            opponent_id=self.get_id(),
            elo_movement=compute_elo_movement(
                player_b.score, self.score, not player_a_won
            ),
        )

        db.session.add(new_match)
        db.session.add(match_history_player_a)
        db.session.add(match_history_player_b)

        self.score += match_history_player_a.elo_movement
        player_b.score += match_history_player_b.elo_movement
        db.session.commit()


class UserMatchHistory(db.Model):
    __tablename__ = "user_match_history"

    id = Column("user_match_history_id", Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    opponent_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    elo_movement = Column(Integer, nullable=False)

    player = db.relationship("User", foreign_keys=[player_id])
    opponent = db.relationship("User", foreign_keys=[opponent_id])
