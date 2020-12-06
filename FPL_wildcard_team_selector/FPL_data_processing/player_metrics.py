import pandas as pd
from FPL_wildcard_team_selector.FPL_data_collection import get_future_fixtures_info, fpl_teams_dict

def get_players_ROI(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "return on investment" metric which is: ROI = form/cost 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'ROI'] = players_info['form']/players_info['now_cost']
 

def get_players_future_games_scores(players_info, Num_Future_Games_To_Analyze, fpl_fixtures_info_api_url:str):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "future games score" metric which is a measure of the difficulty of the games coming up in the near future

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        Num_Future_Games_To_Analyze(int): number of future games to analyze
        fpl_fixtures_info_api_url (str): FPL api url for all fixture information
    '''
    players_info.loc[:,'Future Games Score'] = 0
    fixtures_info_df = get_future_fixtures_info(fpl_fixtures_info_api_url)

    future_fixtures_difficulty_dict = {}
    for key in fpl_teams_dict:
        team_specific_fixtures_info_df = fixtures_info_df[(fixtures_info_df['team_a']==int(key)) | (fixtures_info_df['team_h']==int(key))]
        team_specific_match_difficuty_list = []
        for i in range(Num_Future_Games_To_Analyze):
            home_team = team_specific_fixtures_info_df['team_h'].iloc[i]
            away_team = team_specific_fixtures_info_df['team_a'].iloc[i]
            if home_team == int(key):
                match_difficulty = team_specific_fixtures_info_df['team_h_difficulty'].iloc[i]
            elif away_team == int(key):
                match_difficulty = team_specific_fixtures_info_df['team_a_difficulty'].iloc[i]
            else:
                raise ValueError("using corrupted data frames, please check your sources")
            team_specific_match_difficuty_list.append(match_difficulty)
        fixtures_difficulty_mean = sum(team_specific_match_difficuty_list) / len(team_specific_match_difficuty_list)
        future_fixtures_difficulty_dict[key] = fixtures_difficulty_mean

    Num_Players = len(players_info.index)
    for i in range(Num_Players):
        players_team = players_info.loc[i,'team']
        players_next_n_games_difficulty_mean = future_fixtures_difficulty_dict[str(players_team)]
        players_info.loc[i,'Future Games Score'] = (5-players_next_n_games_difficulty_mean)
