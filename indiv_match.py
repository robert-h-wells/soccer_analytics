#=========================================================================================================================#
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation
import json
from shutil import copyfile
from pandas import json_normalize

import tools as tl
import plots as pl
import ml_test as mlt
import ml_tools as ml
#=========================================================================================================================#\

def main():
    """
    data contains json information 
    poss_list contains start and end data endices for each possesion  (focusing on Arsenal) 7/16
    poss_data/poss_name_data gives the id/name of each player and event type for paths
    """

    with open('game_data/44.json') as f:
        match_data = json.load(f)

    match_data = sorted(match_data, key=lambda x:x['match_week'])
    # read in game file data
    data = []
    for i in range(len(match_data)):
        if (match_data[i]['home_team']['home_team_id'] == 1 
            or match_data[i]['away_team']['away_team_id']) == 1:
                
            with open(str('game_data/'+str(match_data[i]['match_id'])+'.json')) as f:
                data2= json.load(f)
                f.close()

            data.append(data2)

    # Make json and df of the game data
    chosen_match_val = 0
    chosen_data = data[chosen_match_val]
    df_event = json_normalize(chosen_data, sep = "_")
    df_event = df_event.drop(columns=['id'])

    # find data ranges of possession for each team and create list of players
    poss_list, player_list = tl.get_poss_player_list(chosen_data)

    print('Number of players',len(player_list))
    for i in range(len(player_list)):
        print(i,player_list[i][1])

    # map with starting XI positions and initials
    if chosen_data[0]['team']['id'] == 1:  # Home Team
        chosen = chosen_data[0]
        opponent = chosen_data[1]
        scoreline = (str(match_data[chosen_match_val]['home_score'])+' - '
                    +str(match_data[chosen_match_val]['away_score']))
    else:           # Away Team
        chosen = chosen_data[1]
        opponent = chosen_data[0]
        scoreline = (str(match_data[chosen_match_val]['away_score'])+' - '
                    +str(match_data[chosen_match_val]['home_score']))
    
    print() ; print('=============================')
    print(chosen['team']['name']+' vs ' +opponent['team']['name'])  
    print('{:^18s}'.format(scoreline))
    print('=============================') ; print()

    # Match statistics
    tl.match_statistics(df_event)

    player_initials = pl.get_start_map(chosen)

    # list of each player and event in each possession pathway
    poss_data, poss_name_data = tl.get_poss_data(chosen_data,poss_list,player_list)

    # heat map of all touches
    player_pos, touch_cluster = tl.get_touch_data(df_event,player_list)
    #pl.heat_map(df_event,player_list,player_pos,touch_cluster)
    #pl.team_heat_map(player_pos,player_initials)
    #tl.cluster_touch_data(player_list,player_pos,touch_cluster)

    # pass lists and map, set to 1 for indiv pass maps
    pass_data, pass_data_recip, pass_cluster = tl.get_pass_data(player_list,df_event)
    ##pl.indiv_pass_map(pass_data,player_list,1)
    pl.pass_network(pass_data,player_list,player_pos,pass_cluster)
    #pl.pass_map(pass_data_recip,player_list,player_pos,player_initials,4)
    tl.cluster_pass_data(pass_data,player_list,player_pos,pass_cluster)


    # Determine beginning location of paths -> sort based on y and x
    path_start_pos, path_start_val = tl.get_path_pos(chosen_data,poss_list)

    # Plot contour map for starting positions of each pathway
    #pl.get_path_pos_plot(path_start_val)

    # determine pathway points for each possession
    poss_score = tl.get_path_score(chosen_data,poss_list)

    # determine player score (sum of pathway score) and number of pathways they are in
    indiv_score, player_in_path, event_in_path = tl.get_indiv_score(player_list,poss_data,poss_score)


    #==== sort data by length, number of players, etc. ====#

    # list of player names
    nam = [x[1] for x in player_list]

    # list of important events
    event_nam = ['Dribble','Shot','Dribbled_past','Carry']

    # find the length of each pathway
    path_length = np.zeros((len(poss_score)))
    for i in range(len(poss_score)):
        path_length[i] = len([x[1] for x in poss_data[i]])

    # number of unique players in each pathway
    num_players = np.zeros((len(poss_score)))
    for i in range(len(poss_score)):
        num_players[i] = len(set([x[0] for x in poss_data[i]]))

        # Make pandas dataframe of parameters
    df_nam = (['Path_length','Num_players',*(str(i) for i in nam),'Dribble','Shot','Dribbled_past',
                'Carry','Start_val_x','Start_val_y','Score'])
    df_pre = ([path_length,num_players,*(i for i in player_in_path),*(j for j in event_in_path),
                [j[0] for j in path_start_val],[j[1] for j in path_start_val],poss_score])

    df = pd.DataFrame(np.transpose(df_pre),columns=df_nam)

    #================= Examine the data to find degeneracy of attributes ==================#
    
    # length vs score, num players vs score, length and num players vs score
    dat = tl.get_path_info(path_length,num_players,poss_score)
    values_length, values_num_players, values_all, values_total = dat

    # find the percentage of each possesion point at pathway length and num players
    percent_poss_score = tl.get_percent_poss_score(values_all,values_total)

    val_data = [values_length,values_num_players]
    list_data = [poss_list, player_list]

    #ml.ml_visual(df,val_data,percent_poss_score,list_data,nam,event_nam)

    #mlt.ml_models(df,df_nam,nam,event_nam)
    #==================================================================================#

    plt.show()
    
    # plot the possession by highest scoring pathways
    sort_poss_list = [x for _,x in sorted(zip(poss_score,poss_list), reverse=True)]
    sort_poss_score = sorted(poss_score, reverse=True)

    for ii in range(3,2):
        fig, ax=plt.subplots()
        pl.draw_pitch(ax)
        plt.ylim(100, -10)
        pl.plot_pass_path(chosen_data,sort_poss_list[ii][0],sort_poss_list[ii][1])

        plt.ylim(80, 0)
        plt.xlim(0, 120)
        plt.show()
#=========================================================================================================================#


if __name__ == "__main__":
    main()