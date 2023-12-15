POINTS_DICT = {
    "normal_victory": [6, round(5, 5), 5, 4, 3, 2, 1, round(0, 5), 0],
    "normal_defeat": [-5, round(-4, 5), -4, -3, -2, -1, round(-0.5), 0, 0],
    "anormal_victory": [6, 7, 8, 10, 13, 17, 22, 28, 40],
    "anormal_defeat": [-5, -6, -7, -8, -10, round(-12, 5), -16, -20, -29],
}


def tier_index(diff: int) -> int:
    """Return the index of the points dict that should be used, based on the score difference provided.

    Parameters
    ----------
    diff : int
        The score diff between two players

    Returns
    -------
    int
        The index of the POINT_DICT that should be used to compute ELO movement
    """
    thresholds = [
        (0, 24),
        (25, 49),
        (50, 99),
        (100, 149),
        (150, 199),
        (200, 299),
        (300, 399),
        (400, 499),
        (500, 999999999999),
    ]
    for i, (t1, t2) in enumerate(thresholds):
        if t1 <= diff <= t2:
            return i


def compute_elo_movement(player_score: int, opponent_score: int, is_victorious: bool) -> int:
    diff = abs(player_score - opponent_score)
    index_diff = tier_index(diff)
    if is_victorious:
        if player_score >= opponent_score:
            return POINTS_DICT["normal_victory"][index_diff]
        else:
            return POINTS_DICT["anormal_victory"][index_diff]
    else:
        if opponent_score >= player_score:
            return POINTS_DICT["normal_defeat"][index_diff]
        else:
            return POINTS_DICT["anormal_defeat"][index_diff]
