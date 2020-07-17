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

  with open('3749052.json') as f:
      data = json.load(f)

  switch = 0
  prev_switch = 1
  prev_poss = data[1]['possession']
  poss_list = []

  # find data ranges of possession for each team
  for i in range(2,len(data)):
    #print(i,data[i]['possession_team']['name'],data[i]['possession'],prev_switch)
    if data[i]['possession'] != data[i-1]['possession']:
      switch += 1
      if data[i-1]['possession_team']['name'] == 'Arsenal':
        poss_list.append([prev_switch,i])

      prev_switch = i

  print(data[101])
  print('switch',switch)

  #for i in range(len(poss_list)):
  #  print(poss_list[i])

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
  #print(poss_score)
  #print(poss_list)

  ## use techniques of machine learning to find the features that make the highest scoring possession pathways ##
  # sort by length, number of players, etc.

  # find player score (score of all the pathways they are in)


  # plot the possession pathways 
  sort_poss_list = [x for _,x in sorted(zip(poss_score,poss_list), reverse=True)]
  sort_poss_score = sorted(poss_score, reverse=True)


  for ii in range(0,3):
    fig, ax=plt.subplots()
    pl.get_pitch()
    pl.plot_pass_path(data,sort_poss_list[ii][0],sort_poss_list[ii][1])
    
  plt.show()
#=========================================================================================================================#


if __name__ == "__main__":
    main()