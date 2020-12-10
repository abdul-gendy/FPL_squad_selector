import pandas as pd
from FPL_wildcard_team_selector.FPL_data_collection import get_future_fixtures_info, fpl_teams_dict, load_teams_data_from_understat


def get_players_ROI(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "return on investment" metric which is: ROI = form/cost 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'ROI'] = players_info['form']/players_info['now_cost']


def get_npxG90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "expected goals per 90" metric which is: xG90 = (total xG/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'npxG90'] = (players_info['npxG'] * 90)/players_info['minutes']


def get_xA90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "expected assist per 90" metric which is: xA90 = (total xA/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'xA90'] = (players_info['xA'] * 90)/players_info['minutes']


def get_players_future_games_attacking_ease(players_info, Num_Future_Games_To_Analyze, fpl_fixtures_info_api_url:str, teams_info_understat_url:str):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "future games score" metric which is a measure of the difficulty of the games coming up in the near future

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        Num_Future_Games_To_Analyze(int): number of future games to analyze
        fpl_fixtures_info_api_url (str): FPL api url for all fixture information
    '''
    players_info.loc[:,'future games attacking ease'] = 0
    fixtures_info_df = get_future_fixtures_info(fpl_fixtures_info_api_url)
    teams_info_understat_url = load_teams_data_from_understat(teams_info_understat_url)
    Num_Players = len(players_info.index)
    for i in range(Num_Players):
        players_team = players_info.loc[i,'team']
        player_specific_fixtures_info_df = fixtures_info_df[(fixtures_info_df['team_a']==int(players_team)) | (fixtures_info_df['team_h']==int(players_team))]
        player_specific_Attacking_ease_list = []
        for j in range(Num_Future_Games_To_Analyze):
            home_team = player_specific_fixtures_info_df['team_h'].iloc[j]
            away_team = player_specific_fixtures_info_df['team_a'].iloc[j]
            if home_team == int(players_team):
                match_ease = ((players_info.loc[i, 'npxG90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(away_team)]])
                            + (players_info.loc[i, 'xA90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(away_team)]]))
            elif away_team == int(players_team):
                match_ease = ((players_info.loc[i, 'npxG90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(home_team)]])
                            + (players_info.loc[i, 'xA90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(home_team)]]))
            else:
                raise ValueError("using corrupted data frames, please check your sources")
            player_specific_Attacking_ease_list.append(match_ease)
        fixtures_defending_ease_mean = sum(player_specific_Attacking_ease_list) / len(player_specific_Attacking_ease_list)
        players_info.loc[i,'future games attacking ease'] = fixtures_defending_ease_mean


def get_players_future_games_defending_ease(players_info, Num_Future_Games_To_Analyze, fpl_fixtures_info_api_url:str, teams_info_understat_url:str):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "future games score" metric which is a measure of the difficulty of the games coming up in the near future

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        Num_Future_Games_To_Analyze(int): number of future games to analyze
        fpl_fixtures_info_api_url (str): FPL api url for all fixture information
    '''
    players_info.loc[:,'future games defending ease'] = 0
    fixtures_info_df = get_future_fixtures_info(fpl_fixtures_info_api_url)
    teams_info_understat_url = load_teams_data_from_understat(teams_info_understat_url)
    future_fixtures_defending_ease_dict = {}

    for key in fpl_teams_dict:
        team_specific_fixtures_info_df = fixtures_info_df[(fixtures_info_df['team_a']==int(key)) | (fixtures_info_df['team_h']==int(key))]
        team_specific_defending_ease_list = []
        for i in range(Num_Future_Games_To_Analyze):
            home_team = team_specific_fixtures_info_df['team_h'].iloc[i]
            away_team = team_specific_fixtures_info_df['team_a'].iloc[i]
            if home_team == int(key):
                match_ease = teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(home_team)]] * teams_info_understat_url.loc['npxG90',fpl_teams_dict[str(away_team)]]
            elif away_team == int(key):
                match_ease = teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(away_team)]] * teams_info_understat_url.loc['npxG90',fpl_teams_dict[str(home_team)]]
            else:
                raise ValueError("using corrupted data frames, please check your sources")
            team_specific_defending_ease_list.append(match_ease)
        fixtures_defending_ease_mean = sum(team_specific_defending_ease_list) / len(team_specific_defending_ease_list)
        future_fixtures_defending_ease_dict[key] = fixtures_defending_ease_mean

    Num_Players = len(players_info.index)
    for i in range(Num_Players):
        players_team = players_info.loc[i,'team']
        players_next_n_games_defending_ease_mean = future_fixtures_defending_ease_dict[str(players_team)]
        players_info.loc[i,'future games defending ease'] = players_next_n_games_defending_ease_mean
