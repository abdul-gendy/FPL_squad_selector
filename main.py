import sys
from FPL_wildcard_team_selector import play_wildcard


if __name__ == "__main__":
    formation = int(sys.argv[1])
    minimum_number_of_minutes_played = int(sys.argv[2])
    Number_of_future_games_to_analyze = int(sys.argv[3])
    play_wildcard(formation, minimum_number_of_minutes_played, Number_of_future_games_to_analyze)