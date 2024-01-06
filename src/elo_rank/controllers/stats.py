from typing import List, Optional
from flask_login import login_required, current_user
from flask import Blueprint, flash, redirect, render_template, request, url_for


from elo_rank.models.users import User

stats = Blueprint("stats", __name__)


@stats.route("/leaderboard")
@login_required
def leaderboard():
    players: User = User.query.all()
    players.sort(key=lambda p: p.score, reverse=True)
    players = [
        {"position": i+1, "link": user.link, "score": user.score}
        for i, user in enumerate(players)
    ]
    return render_template("leaderboard.html", players=players)
