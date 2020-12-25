import sys
from FPL_wildcard_team_selector import play_wildcard


if __name__ == "__main__":
    formation = 433
    minimum_number_of_minutes_played = 600
    number_of_future_games_to_analyze = 3
    account_for_penalties = True
    play_wildcard(formation, minimum_number_of_minutes_played, number_of_future_games_to_analyze, account_for_penalties)
