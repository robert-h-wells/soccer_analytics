#=========================================================================================================================#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation
import json
from scipy.interpolate import griddata
from shutil import copyfile

import tools as tl
import plots as pl
import ml_test as ml

#=========================================================================================================================#

def main():
  """
  data contains json information 
  poss_list contains start and end data endices for each possesion  (focusing on Arsenal) 7/16
  poss_data/poss_name_data gives the id/name of each player and event type for paths
  """

  with open('game_data/44.json') as f:
    match_data = json.load(f)

  #if files have not been copied to correct directory
  if 1==0:
    tl.copy_files_tools(match_data)

  # read in game file data
  data = []
  for i in range(len(match_data)):
    with open(str('game_data/'+str(match_data[i]['match_id'])+'.json')) as f:
      data2= json.load(f)
      f.close()

    data.extend(data2)

  # find data ranges of possession for each team and create list of players
  poss_list, player_list = tl.get_poss_player_list(data)
  print('Number of games',len(match_data))
  print('Number of players',len(player_list))

  for i in range(len(player_list)):
    print(i,player_list[i][1])

  # create list of each player and event in each possession pathway
  poss_data, poss_name_data = tl.get_poss_data(data,poss_list,player_list)

  # TO-DO, Determine beginning location of paths -> sort based on y and x
  path_start_pos, path_start_val = tl.get_path_pos(data,poss_list)

  # determine pathway points for each possession
  poss_score = tl.get_path_score(data,poss_list)

  # determine player score (sum of pathway score) and number of pathways they are in
  indiv_score, player_in_path, event_in_path = tl.get_indiv_score(player_list,poss_data,poss_score)


  #==== sort data by length, number of players, etc. ====#

  # find the length of each pathway
  path_length = np.zeros((len(poss_score)))
  for i in range(len(poss_score)):
    path_length[i] = len([x[1] for x in poss_data[i]])

  # number of unique players in each pathway
  num_players = np.zeros((len(poss_score)))
  for i in range(len(poss_score)):
    num_players[i] = len(set([x[0] for x in poss_data[i]]))

  ## score, length of path, number of players, is player present
  total_data_ = ([path_length,num_players,([i for i in player_in_path]),
                ([j for j in event_in_path]),path_start_val,poss_score])
  total_data = np.transpose(total_data_)
  
  # list of player names
  nam = [x[1] for x in player_list]

  #================= Examine the data to find important attributes ==================#
  
  # determine the degeneracy of combinations of the 3 important attributes
  # length vs score, num players vs score, length and num players vs score
  dat = tl.get_path_info(path_length,num_players,poss_score)
  values_length, values_num_players, values_all, values_total = dat

  # find the percentage of each possesion point at pathway length and num players
  percent_poss_score = tl.get_percent_poss_score(values_all,values_total)
  #==================================================================================#
  
  # plot the possession by highest scoring pathways
  sort_poss_list = [x for _,x in sorted(zip(poss_score,poss_list), reverse=True)]
  sort_poss_score = sorted(poss_score, reverse=True)

  for ii in range(3,2):
    fig, ax=plt.subplots()
    pl.get_pitch()
    plt.ylim(100, -10)
    pl.plot_pass_path(data,sort_poss_list[ii][0],sort_poss_list[ii][1])

    #plt.gca().invert_yaxis()
    plt.show()
  #=============================================================================================================#
  
  val_data = [values_length,values_num_players]
  list_data = [poss_list, player_list]

  ml.ml_run(total_data_,val_data,percent_poss_score,list_data,nam)
#=========================================================================================================================#


if __name__ == "__main__":
    main()