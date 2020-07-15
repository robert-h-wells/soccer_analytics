import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import json

import tools as tl

# this file will make a list of the path routes
# will make paths before possession switches

with open('3749052.json') as f:
    data = json.load(f)

switch = 0
prev_switch = 1
prev_poss = data[1]['possession']
poss_list = []

# find data ranges of possession for each team
for i in range(2,len(data)):
  if data[i]['possession'] != data[i-1]['possession']:
    switch += 1
    if data[i]['possession_team']['name'] == 'Arsenal':
      poss_list.append([prev_switch,i])

    prev_switch = i

print(data[101])
print('switch',switch)

for ii in range(4,7):
  fig, ax=plt.subplots()
  tl.get_pitch()
  for i in range(poss_list[ii][0], poss_list[ii][1]):
    print(ii,i,data[i]['type']['name'],data[i]['player']['name'],data[i]['timestamp'],data[i]['possession_team']['name'])
    #print(data[i]) ; print('')
    value = data[i]['type']['name']

    if value == 'Pass':
      print('pass')
      X1 = data[i]['location'][0]
      Y1 = data[i]['location'][1]
      
      X2 = data[i]['pass']['end_location'][0]
      Y2 = data[i]['pass']['end_location'][1]

      if 'outcome' in data[i]['pass']:
        plt.plot(X1,Y1,'o',color='gray')
        plt.plot([X1,X2],[Y1,Y2],color='red')
        plt.plot(X2,Y2,'X',color='red')
      else:
        plt.plot(X1,Y1,'o',color='gray')
        plt.plot([X1,X2],[Y1,Y2],color='green')
        plt.plot(X2,Y2,'o',color='green')
    
    elif value == 'Dribble' or value == 'Ball Receipt*':
      print('dribble',' ',value)
      X1 = data[i]['location'][0]
      Y1 = data[i]['location'][1]
      plt.plot(X1,Y1,'D',color='blue')

    elif value == 'Shot':
      print('shot')
      X1 = data[i]['location'][0]
      Y1 = data[i]['location'][1]
      plt.plot(X1,Y1,'*',color='yellow')

    elif value == 'Pressure' or value == 'Duel' or value == 'Dribbled Past':
      pass
    
    else:
      print('other ',value)
      X1 = data[i]['location'][0]
      Y1 = data[i]['location'][1]
      plt.plot(X1,Y1,'o',color='orange')

    plt.title(data[i]['timestamp'])
    plt.pause(1.0)

plt.show()