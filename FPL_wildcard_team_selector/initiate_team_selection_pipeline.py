import FPL_wildcard_team_selector.FPL_data_collection as dc
import FPL_wildcard_team_selector.FPL_data_processing as dp
import FPL_wildcard_team_selector.FPL_data_visualization as dv
import os

def play_wildcard(formation_to_draw:int, minimum_number_of_minutes_played=540, number_of_future_games_to_analyze=3, account_for_penalties=True):
    valid_formations = [433, 442, 352, 343]
    if formation_to_draw not in valid_formations:
        raise ValueError("Undefined formation requested. Please select one of the following formations: 442, 433, 352, 343")

    fpl_main_api_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    fpl_fixtures_info_api_url = 'https://fantasy.premierleague.com/api/fixtures/'
    understat_players_and_teams_info_url = 'https://understat.com/league/EPL/2020'
    
    print("currently selecting the best 15 players for your wildcard, please be patient. This may take a few minutes")
    fpl_players_info, fpl_teams_info = dc.parse_main_FPL_API(fpl_main_api_url)
    understat_players_info = dc.load_player_data_from_understat(understat_players_and_teams_info_url, minimum_number_of_minutes_played)
    dc.combine_data_from_fpl_understat(fpl_players_info,understat_players_info)

    fpl_players_info = fpl_players_info[(fpl_players_info['minutes'] > minimum_number_of_minutes_played) & (fpl_players_info['chance_of_playing_next_round'] != 0)]
    fpl_players_info.reset_index(inplace=True)

    columns_to_turn_to_floats = ['form','points_per_game','ict_index','ep_next', 'npxG', 'xA','xG','npg','assists']
    fpl_players_info = dp.turn_series_to_float(fpl_players_info, columns_to_turn_to_floats)

    dp.add_players_full_name(fpl_players_info)
    dp.get_players_ROI(fpl_players_info)
    dp.get_G90(fpl_players_info)
    dp.get_xG90(fpl_players_info)
    dp.get_npxG90(fpl_players_info)
    dp.get_npg90(fpl_players_info)
    dp.get_A90(fpl_players_info)
    dp.get_xA90(fpl_players_info)
    dp.get_assisting_ability(fpl_players_info)
    dp.get_chance_conversion_ability(fpl_players_info, account_for_penalties)
    dp.get_players_future_games_defending_ease(fpl_players_info, number_of_future_games_to_analyze, account_for_penalties, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)
    dp.get_players_future_games_attacking_ease(fpl_players_info, number_of_future_games_to_analyze, account_for_penalties, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)

    #Future games attacking ease, Future games defending ease, chance conversion ability, assisting ability, ROI
    srikers_midfielders_scoring_weights = [0.5, 0.0, 0.1, 0.1, 0.2] 
    defenders_goalies_scoring_weights = [0.35, 0.15, 0.1, 0.1, 0.2]

    dp.calculate_players_scores_weighted_avg_sum(fpl_players_info, srikers_midfielders_scoring_weights, defenders_goalies_scoring_weights)
    ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left = dp.team_selection_using_linear_optimization(fpl_players_info)

    if formation_to_draw == 442:
        visualization_object = dv.visualize_team_selection_442(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 433:
        visualization_object = dv.visualize_team_selection_433(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 352:
        visualization_object = dv.visualize_team_selection_352(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 343:
        visualization_object = dv.visualize_team_selection_343(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    else:
        raise ValueError("Undefined formation requested. Please select one of the following formations: 442, 433, 352, 343")

    fpl_players_info.loc[:,'now_cost'] = fpl_players_info['now_cost'] * 0.1
    csv_path = os.path.join(os.getcwd(),'FPL_detailed_players_stats.csv')
    columns_to_add_to_csv = ['web_name','now_cost','total_points','pts90','ROI','chance_of_playing_next_round','minutes',
                            'goals_scored','npg','xG', 'npxG', 'npxG90', 'npG90', 'xG90', 'G90', 'chance_conversion_ability', 'assists',
                            'xA', 'xA90', 'A90', 'assisting_ability','future games attacking ease', 'future games defending ease', 'Algorithm Score']
    fpl_players_info[columns_to_add_to_csv].to_csv(csv_path)
  
    print("Team selection is done. To exit the program, you can close the graphics tab")
    visualization_object.run_visualization()
