import pandas as pd
from FPL_data_collection import get_players_future_games_info


def get_players_ROI(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "return on investment" metric which is: ROI = form/cost 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info['ROI'] = players_info['form']/players_info['now_cost']
 

def get_players_future_games_scores(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "future games score" metric which is a measure of the difficulty of the games coming up in the near future

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info['Future Games Score'] = 0
    Num_Players = len(players_info.index)
    Num_Future_Games_To_Analyze = 4
    for i in range(Num_Players):
        Player_id = players_info['id'].iloc[i]
        Player_Fixtures = get_players_future_games_info(Player_id)
        Difficulty_Mean = Player_Fixtures['difficulty'].iloc[0:Num_Future_Games_To_Analyze].mean(axis=0)
        #players_info['Future Games Score'].iloc[i] = (5-Difficulty_Mean)
        players_info.loc['Future Games Score', i] = (5-Difficulty_Mean)
