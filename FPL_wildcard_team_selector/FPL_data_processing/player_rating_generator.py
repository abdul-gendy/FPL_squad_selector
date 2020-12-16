import pandas as pd
from .utilities import set_range_one_to_ten


def calculate_players_scores_weighted_avg_sum(players_info, srikers_midfielders_scoring_weights, defenders_goalies_scoring_weights):
    '''
    takes in a DataFrame containing all the players info and stats, and a list containing all the weights that will be used in the 
    weighted sum. Adds a column called Algorithm Score to the existing Dataframe which is the final score out of 10 given to each player

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        weights (list): list containing the weights of [form, ROI, ptspergame, ict, ep_next, future games score] in that order
    '''
    columns_to_normalize = ['form','points_per_game','ict_index','ep_next','ROI','future games attacking ease','future games defending ease', 'npxG', 'xA']
    set_range_one_to_ten(players_info, columns_to_normalize)

    #Future Games attacking ease, Future Games defending ease
    defenders_goalies_scoring_weights_sum = defenders_goalies_scoring_weights[0] + defenders_goalies_scoring_weights[1] 
    srikers_midfielders_scoring_weights_sum = srikers_midfielders_scoring_weights[0] + srikers_midfielders_scoring_weights[1]

    players_info.loc[:,'Algorithm Score'] = 0

    players_info.loc[players_info['element_type'] == 1,'Algorithm Score'] = ((players_info['future games attacking ease'].multiply(defenders_goalies_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(defenders_goalies_scoring_weights[1]))) / defenders_goalies_scoring_weights_sum  
    players_info.loc[players_info['element_type'] == 2,'Algorithm Score'] = ((players_info['future games attacking ease'].multiply(defenders_goalies_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(defenders_goalies_scoring_weights[1]))) / defenders_goalies_scoring_weights_sum  
    players_info.loc[players_info['element_type'] == 3,'Algorithm Score'] = ((players_info['future games attacking ease'].multiply(srikers_midfielders_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(srikers_midfielders_scoring_weights[1]))) / srikers_midfielders_scoring_weights_sum  
    players_info.loc[players_info['element_type'] == 4,'Algorithm Score'] = ((players_info['future games attacking ease'].multiply(srikers_midfielders_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(srikers_midfielders_scoring_weights[1]))) / srikers_midfielders_scoring_weights_sum  
    
    #players_info.loc[:,'Algorithm Score'] = ((players_info['npxG'].multiply(weights[0]))                         
    #                                    + (players_info['future games attacking ease'].multiply(weights[1]))) / sum_of_weights                       
    players_info.sort_values(by='Algorithm Score', inplace = True, ascending=False) 
