def match_probability(team1_win_prob, team2_win_prob):
    draw_prob = 1 - (team1_win_prob + team2_win_prob)
    return {"Team 1 Wins": team1_win_prob, "Team 2 Wins": team2_win_prob, "Draw": draw_prob}

print(match_probability(0.4, 0.5))