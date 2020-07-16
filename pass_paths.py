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
  poss_score = len(poss_list)*[None]
  for i in range(2,len(poss_list)):
  #for i in range(2,10):
    val = poss_list[i][1]-1

    if 1==0:
      try:
        print(data[val]['type']['name'],data[val]['player']['name'],data[val]['play_pattern']['name'],data[val]['possession_team']['name'],data[val]['possession'])
        print(data[val+1]['type']['name'],data[val+1]['player']['name'],data[val+1]['play_pattern']['name'],data[val+1]['possession_team']['name'],data[val+1]['possession'])
        print('')
        if data[val+1]['possession_team']['name'] != 'Arsenal':
          print('whoops bad result')
      except KeyError:
        pass

    try:

      if data[val+1]['possession_team']['name'] == 'Arsenal':  # possesion stays
        if data[val+1]['play_pattern']['id'] == 2:  # caused a corner kick
          poss_score[i] = 3
        elif data[val+1]['play_pattern']['id'] == 3:  # caused a free kick
          poss_score[i] = 2
        elif data[val+1]['play_pattern']['id'] == 4:  # caused a throw in
          poss_score[i] = 1
        elif data[val+1]['play_pattern']['id'] == 7:  # caused a goal kick
          poss_score[i] = 1
        else:
          print('NEW TYPE')
        
      elif data[val+1]['possession_team']['name'] != 'Arsenal':  # possesion changes
        if data[val+1]['play_pattern']['id'] == 2:  # caused a corner kick 
          poss_score[i] = -3
        elif data[val+1]['play_pattern']['id'] == 3:  # caused a free kick
          poss_score[i] = -2
        elif data[val+1]['play_pattern']['id'] == 4:  # caused a throw in
          poss_score[i] = -1
        elif data[val+1]['play_pattern']['id'] == 7:  # caused a goal kick
          poss_score[i] = -1

        elif data[val+1]['play_pattern']['id'] == 1:  # open play, gave ball away
            poss_score[i] = -2

        elif:
          # this is not done yet, bed
          print(data[val]['goalkeeper']['type']['name'])

        else:
          print('NEW NEW')
          print(data[val+1]['play_pattern']['name'])
          print(data[val]['type']['name'],data[val]['play_pattern']['name'])
          print(data[val]['goalkeeper']['type']['name'])
          #print(data[val-1])
          print('')

      else:
        print('WTF')

    except KeyError as e:
      print('========================================================')
      print(str(e))
      print(data[val+1])
      print('========================================================')

  print(poss_score)


  # plot the possession pathways
  for ii in range(12,10):
    fig, ax=plt.subplots()
    pl.get_pitch()
    pl.plot_pass_path(data,poss_list[ii][0],poss_list[ii][1])
    
  plt.show()
#=========================================================================================================================#


if __name__ == "__main__":
    main()