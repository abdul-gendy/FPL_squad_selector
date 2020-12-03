import sys
from FPL_wildcard_team_selector import play_wildcard


if __name__ == "__main__":
    formation = int(sys.argv[1])
    play_wildcard(formation)