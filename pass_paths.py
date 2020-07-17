#=========================================================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import json

import tools as tl
import plots as pl
#=========================================================================================================================#

def main():
  # data contains json information 
  # poss_list contains start and end data endices for each possesion  (focusing on Arsenal) 7/16
  # poss_data/poss_name_data gives the id/name of each player and event type for paths 

  with open('3749052.json') as f:
      data = json.load(f)

  # find data ranges of possession for each team and create list of players
  poss_list, player_list = tl.get_poss_player_list(data)

  # create list of each player and event in each possession pathway
  poss_data, poss_name_data = tl.get_poss_data(data,poss_list)

  # determine pathway points for each possession
  poss_score = tl.get_path_score(data,poss_list)
  print(poss_score)
  
  # determine player score (sum of pathway score) and number of pathways they are in
  indiv_score = tl.get_indiv_score(player_list,poss_data,poss_score)

  for i in range(len(player_list)):
    print(player_list[i][1],player_list[i][0],indiv_score[i][0],indiv_score[i][1]) 


  ## use techniques of machine learning to find the features that make the highest scoring possession pathways ##
  # sort by length, number of players, etc.
  total_data = [poss_score,poss_data,]


  # plot the possession by highest scoring pathways
  sort_poss_list = [x for _,x in sorted(zip(poss_score,poss_list), reverse=True)]
  sort_poss_score = sorted(poss_score, reverse=True)

  for ii in range(3,5):
    fig, ax=plt.subplots()
    pl.get_pitch()
    plt.ylim(100, -10)
    pl.plot_pass_path(data,sort_poss_list[ii][0],sort_poss_list[ii][1])

  #plt.gca().invert_yaxis()
  plt.show()
#=========================================================================================================================#


if __name__ == "__main__":
    main()