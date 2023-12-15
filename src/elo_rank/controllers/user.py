from typing import List, Optional
from flask_login import login_required, current_user
from flask import Blueprint, flash, redirect, render_template, request, url_for
from elo_rank.models.matches import Match

from elo_rank.models.users import User, UserMatchHistory

user = Blueprint("user", __name__)


@user.route("/profile")
@login_required
def profile(user_id: Optional[int] = None):
    match_history: List[UserMatchHistory] = UserMatchHistory.query.filter_by(
        player_id=current_user.get_id()
    ).all()

    return render_template("user.html", matches=match_history)


@user.get("/commit_match")
@login_required
def commit_match():
    users = User.query.all()
    return render_template("commit_match.html", players=[u.email for u in users])


@user.post("/commit_match")
@login_required
def manage_commit_match():
    player_a = current_user
    player_b_email = request.form.get("player_b")
    form_redirection = redirect(url_for("user.commit_match"))

    if player_b_email == player_a.email:
        flash(f"You cannot compete against yourself. Please select another opponent.")
        return form_redirection

    player_b = User.query.filter_by(email=player_b_email).first()
    if not player_b:
        flash(
            f"The user {player_b_email} is unknown. Please create an account with this user in order to save the match details."
        )
        return form_redirection

    set_1 = request.form.get("set_1")
    set_2 = request.form.get("set_2")
    set_3 = request.form.get("set_3")

    if set_1 == "" or set_2 == "":
        flash(f"You have to provide minimum 2 sets in order to commit this match.")
        return form_redirection

    points = {}
    for i, s in enumerate([set_1, set_2, set_3]):
        set_id = i + 1
        try:
            set_point = int(s)
        except ValueError as e:
            if set_id == 3 and s == "":
                set_point = None
            else:
                flash(
                    f"The value provided for set {set_id} ({s}) cannot be converted to an integer."
                )
                return form_redirection

        if set_point == 0:
            flash(
                f"Even if a player did not win any point for the set {set_id}, a zero score cannot be accepted. Give him one point."
            )
            return form_redirection
        points[set_id] = set_point

    try:
        player_a.report_match(player_b, points[1], points[2], points[3])
    except ValueError as e:
        flash(str(e))
        return form_redirection

    return redirect(url_for("user.profile"))
