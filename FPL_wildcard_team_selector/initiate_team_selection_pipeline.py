import sys
from .FPL_data_collection import parse_main_FPL_API, load_player_data_from_understat, combine_data_from_fpl_understat
from .FPL_data_processing import get_players_future_games_attacking_ease, get_players_future_games_defending_ease, set_range_one_to_ten, add_players_full_name, get_xA90, get_npxG90, get_players_ROI, calculate_players_scores_weighted_avg_sum, team_selection_using_linear_optimization, turn_series_to_float
from .FPL_data_visualization import visualize_team_selection_442, visualize_team_selection_352, visualize_team_selection_343, visualize_team_selection_433
import pprint

def play_wildcard(formation_to_draw:int):
    valid_formations = [433, 442, 352, 343]
    if formation_to_draw not in valid_formations:
        raise ValueError("Undefined formation requested. Please select one of the following formations: 442, 433, 352, 343")

    fpl_main_api_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    fpl_fixtures_info_api_url = 'https://fantasy.premierleague.com/api/fixtures/'
    understat_players_and_teams_info_url = 'https://understat.com/league/EPL/2020'
    Number_of_future_games_to_analyze = 3
    
    print("currently selecting the best 15 players for your wildcard, please be patient. This may take a few minutes")
    fpl_players_info, fpl_teams_info = parse_main_FPL_API(fpl_main_api_url)
    understat_players_info = load_player_data_from_understat(understat_players_and_teams_info_url)
    
    combine_data_from_fpl_understat(fpl_players_info,understat_players_info)
    columns_to_turn_to_floats = ['form','points_per_game','ict_index','ep_next', 'npxG', 'xA','xG']
    fpl_players_info = turn_series_to_float(fpl_players_info, columns_to_turn_to_floats)
    pprint.pprint(fpl_players_info)

    add_players_full_name(fpl_players_info)
    get_players_ROI(fpl_players_info)
    get_npxG90(fpl_players_info)
    get_xA90(fpl_players_info)
    get_players_future_games_defending_ease(fpl_players_info, Number_of_future_games_to_analyze, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)
    get_players_future_games_attacking_ease(fpl_players_info, Number_of_future_games_to_analyze, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)

    #npxG, xA, form, pointspergame, ict_index, Future Games Score
    Regular_Scoring_Weights = [0.0, 0.0 , 0.0, 0.0, 0.0, 1.0] 
    calculate_players_scores_weighted_avg_sum(fpl_players_info, Regular_Scoring_Weights)
    pprint.pprint(fpl_players_info)

    ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left = team_selection_using_linear_optimization(fpl_players_info)
    if formation_to_draw == 442:
        visualization_object = visualize_team_selection_442(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 433:
        visualization_object = visualize_team_selection_433(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 352:
        visualization_object = visualize_team_selection_352(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 343:
        visualization_object = visualize_team_selection_343(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    else:
        raise ValueError("Undefined formation requested. Please select one of the following formations: 442, 433, 352, 343")

    print("Team selection is done. To exit the program, you can close the graphics tab")
    visualization_object.run_visualization()
