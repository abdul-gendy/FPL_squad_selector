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
            print(name, ", ", best_match, ",",ratio, '\n')
            player_index = fpl_api_players_info_df.loc[fpl_api_players_info_df['web_name'] == best_match].index[0]
            for stat in understat_relevant_player_stats:
                fpl_api_players_info_df.loc[player_index,stat] = specific_team_players_info_understat.loc[index, stat]

#def manual_combination_for_select_players()