import sys
from FPL_wildcard_team_selector import play_wildcard, generate_player_stats


if __name__ == "__main__":
    minimum_number_of_minutes_played = 900
    number_of_future_games_to_analyze = 3
    account_for_penalties = True
    money_available = 103.7
    #play_wildcard(money_available, minimum_number_of_minutes_played, number_of_future_games_to_analyze, account_for_penalties)
    generate_player_stats(minimum_number_of_minutes_played, number_of_future_games_to_analyze, account_for_penalties)