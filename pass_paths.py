#=========================================================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import json

import tools as tl
import plots as pl

# this file will make a list of the path routes
# will make paths before possession switches
#=========================================================================================================================#

def main():
  # data contains json information 
  # poss_list contains start and end data endices for each possesion  (focusing on Arsenal) 7/16
  # poss_data/poss_name_data gives the id/name of each player and event type for paths 

  with open('3749052.json') as f:
      data = json.load(f)

  switch = 0
  prev_switch = 1
  prev_poss = data[1]['possession']
  poss_list = []
  player_list = []

  # find data ranges of possession for each team
  # create list of all players in the game
  for i in range(len(data)):
    if data[i]['type']['id'] in [19, 35]: # Starting XI and subs
      if data[i]['type']['id'] == 35:
        if data[i]['team']['name'] == 'Arsenal':
          for i in data[i]['tactics'].get('lineup'):
            player_list.append([i['player']['id'],i['player']['name']])
      elif data[i]['type']['id'] == 19:
        if data[i]['team']['name'] == 'Arsenal':
          player_list.append([data[i]['substitution']['replacement']['id'], 
          data[i]['substitution']['replacement']['name']])
    
    elif data[i]['possession'] != data[i-1]['possession']:
      switch += 1
      if data[i-1]['possession_team']['name'] == 'Arsenal':
        poss_list.append([prev_switch,i])

      prev_switch = i

  #print(data[101])
  print('switch',switch)


  # create list of each player and event in each possession pathway
  poss_data = []
  poss_name_data = []
  for i in range(2,len(poss_list)):
    poss_data.append([])
    poss_name_data.append([])
    new_list = [] ; new_name_list = []

    for j in range(poss_list[i][0], poss_list[i][1]):
      try:
        new_list.append([data[j]['player']['id'],data[j]['type']['id']])
        new_name_list.append([data[j]['player']['name'],data[j]['type']['name']])
      except KeyError:
        pass

    poss_data[i-2] = new_list
    poss_name_data[i-2] = new_name_list

  # determine pathway points for each possession
  poss_score = tl.get_path_score(data,poss_list)

  # find player score (score of all the pathways they are in)
  total_data = [poss_score,poss_data]

  indiv_score = []
  for id_val, type_val in player_list:
    score = 0
    for i in range(len(poss_data)):
      if id_val in poss_data[i][0][0]:
        score += poss_score

    indiv_score.append(score)

  print(indiv_score)  
    # would like to just add the score to the player_list
    # player_list[].insert()

  ## use techniques of machine learning to find the features that make the highest scoring possession pathways ##
  # sort by length, number of players, etc.

  #print(poss_data)
  print(np.shape(poss_data))
  print(len(poss_data[0]))

  # plot the possession pathways 
  sort_poss_list = [x for _,x in sorted(zip(poss_score,poss_list), reverse=True)]
  sort_poss_score = sorted(poss_score, reverse=True)


  for ii in range(4,3):
    fig, ax=plt.subplots()
    pl.get_pitch()
    pl.plot_pass_path(data,sort_poss_list[ii][0],sort_poss_list[ii][1])
    
  plt.show()
#=========================================================================================================================#


if __name__ == "__main__":
    main()