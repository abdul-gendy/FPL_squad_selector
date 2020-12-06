import pandas as pd
from .utilities import set_range_one_to_ten


def calculate_players_scores_weighted_avg_sum(players_info, weights):
    '''
    takes in a DataFrame containing all the players info and stats, and a list containing all the weights that will be used in the 
    weighted sum. Adds a column called Algorithm Score to the existing Dataframe which is the final score out of 10 given to each player

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        weights (list): list containing the weights of [form, ROI, ptspergame, ict, ep_next, future games score] in that order
    '''
    #Players_Filtered = players_info[players_info['minutes'] > 270]
    #Midfielder_Final_Filter = Defender_Initial_Filter[Goalies_Initial_Filter['chance_of_playing_next_round'] == 100] 
    columns_to_normalize = ['form','points_per_game','ict_index','ep_next','ROI','Future Games Score']
    set_range_one_to_ten(players_info, columns_to_normalize)

    sum_of_weights = weights[0] + weights[1] + weights[2] + weights[3] + weights[4]
    players_info.loc[:,'Algorithm Score'] = ((players_info['form'].multiply(weights[0])) 
                                        + (players_info['ROI'].multiply(weights[1])) 
                                        + (players_info['points_per_game'].multiply(weights[2]))
                                        + (players_info['ict_index'].multiply(weights[3]))
                                        + (players_info['ep_next'].multiply(weights[4]))                          
                                        + (players_info['Future Games Score'].multiply(weights[5]))) / sum_of_weights                       
    players_info.sort_values(by='Algorithm Score', inplace = True, ascending=False) 
