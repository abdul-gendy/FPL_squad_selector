import pandas as pd
from fuzzywuzzy import process
from .constants import fpl_teams_dict, understat_relevant_player_stats


def combine_data_from_fpl_understat(fpl_api_players_info_df, understat_url_players_info_df):
    '''
    Adds the required stats from the understat url to the fpl api players info Dataframe 

    Parameters:
        fpl_api_players_info_df (DataFrame): Dataframe containing players info from fpl api
        understat_url_players_info_df (DataFrame): Dataframe containing players info from understat
    '''
    for stat in understat_relevant_player_stats:
        fpl_api_players_info_df.loc[:, stat] = 0

    for key in fpl_teams_dict:
        specific_team_players_info_fpl = fpl_api_players_info_df[fpl_api_players_info_df['team']==int(key)]
        specific_team_players_info_understat = understat_url_players_info_df[understat_url_players_info_df['team_title']==fpl_teams_dict[key]]

        fpl_player_names = specific_team_players_info_fpl['web_name']
        understat_player_names = specific_team_players_info_understat['player_name']

        for index, name in understat_player_names.items():
            best_match, ratio = process.extractOne(name, fpl_player_names.tolist())
            #print(name, ", ", best_match, ",",ratio, '\n')
            player_index = fpl_api_players_info_df.loc[(fpl_api_players_info_df['team']==int(key)) & (fpl_api_players_info_df['web_name'] == best_match)].index[0]
            for stat in understat_relevant_player_stats:
                fpl_api_players_info_df.loc[player_index,stat] = specific_team_players_info_understat.loc[index, stat]
    manual_combination_for_select_players(fpl_api_players_info_df, understat_url_players_info_df)


def manual_combination_for_select_players(fpl_api_players_info_df, understat_url_players_info_df):
    '''
    Adds the required stats from the understat url to the fpl api players info Dataframe. the stats for some players need to be added manually, as 
    fuzzy wuzzy fails to find the correct match between the players name on fpl and understat for these players 

    Parameters:
        fpl_api_players_info_df (DataFrame): Dataframe containing players info from fpl api
        understat_url_players_info_df (DataFrame): Dataframe containing players info from understat
    '''
    manual_addition_players = [('17','Davinson Sánchez','Sánchez'),
                                ('9','James Maddison','Maddison'),('9','James Justin','Justin'),
                                ('8','Bobby Reid','Decordova-Reid'),('8','Franck Zambo','Anguissa')]

    for key, player_name_on_understat, player_name_on_fpl in manual_addition_players:
        specific_team_players_info_fpl = fpl_api_players_info_df[fpl_api_players_info_df['team']==int(key)]
        specific_team_players_info_understat = understat_url_players_info_df[understat_url_players_info_df['team_title']==fpl_teams_dict[key]]

        fpl_player_names = specific_team_players_info_fpl['web_name']
        understat_player_names = specific_team_players_info_understat['player_name']

        if player_name_on_understat in understat_player_names.values:
            #print(player_name_on_understat, 'exists in Dataframe')
            understat_df_player_index = specific_team_players_info_understat.loc[specific_team_players_info_understat['player_name']==player_name_on_understat].index[0]
            fpl_df_player_index = specific_team_players_info_fpl.loc[specific_team_players_info_fpl['web_name'] == player_name_on_fpl].index[0]

            for stat in understat_relevant_player_stats:
                fpl_api_players_info_df.loc[fpl_df_player_index,stat] = specific_team_players_info_understat.loc[understat_df_player_index, stat]
