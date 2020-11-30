from FPL_data_collection import load_json_data_from_FPL_url, parse_main_FPL_API
from FPL_data_processing import calculate_players_scores_weighted_avg_sum, team_selection_using_linear_optimization, turn_series_to_float
from FPL_data_visualization import visualize_team_selection_442, visualize_team_selection_352, visualize_team_selection_343, visualize_team_selection_433


def main():
    FPL_API_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    JSON_Data = load_json_data_from_FPL_url(FPL_API_url)
    players_info, teams_info, events_info = parse_main_FPL_API(JSON_Data)

    columns_to_turn_to_floats = ['form','points_per_game','ict_index','influence','ep_next']
    players_info = turn_series_to_float(players_info, columns_to_turn_to_floats)

    #form, ROI, ptsPerGame, ICT index, ep_next, Future Games Score
    Regular_Scoring_Weights = [0.2, 0.0 , 0.2, 0.1, 0.2, 0.3] 
    players_info = calculate_players_scores_weighted_avg_sum(players_info, Regular_Scoring_Weights)

    ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left = team_selection_using_linear_optimization(players_info)

    visualization_object = visualize_team_selection_343(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    visualization_object.run_visualization()


if __name__ == "__main__":
    print("currently selecting the best team of 15, please be patient")
    main()