import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import json

import tools as tl

# this file will make a list of the time ordered events

with open('7298.json') as f:
    data = json.load(f)

print(data[101])

time_list = []
pass_items = []
player_list = [] 
player_name_list = []
for i in range(len(data)):
    for key,value in data[i]['type'].items():
        if value == 'Pass':
            pass_items.append(data[i])
            time_list.append(data[i]['timestamp'])

print(len(time_list))

numArray = len(time_list)
pass_axes = []
X1 = np.zeros((len(pass_items),2))
X2 = np.zeros((len(pass_items),2)) 
Y1 = np.zeros((len(pass_items),2))  
Y2 = np.zeros((len(pass_items),2))

fig, ax=plt.subplots()
tl.get_pitch()


#for i in range(numArray):
def update(i):
  pass_axes.append([pass_items[i]['location'],pass_items[i]['pass']['end_location']])
  
  X1[i] = [pass_axes[i][0][0],pass_items[i]['player']['id']]
  Y1[i] = [pass_axes[i][0][1],pass_items[i]['player']['id']]
  X2[i] = [pass_axes[i][1][0],pass_items[i]['player']['id']]
  Y2[i] = [pass_axes[i][1][1],pass_items[i]['player']['id']]

  if 'outcome' in pass_items[i]['pass']:
      plt.plot([X1[i,0],X2[i,0]],[Y1[i,0],Y2[i,0]],color='red')
      plt.plot(X2[i,0],Y2[i,0],'X',color='red')
  else:
    plt.plot([X1[i,0],X2[i,0]],[Y1[i,0],Y2[i,0]],color='green')
    plt.plot(X2[i,0],Y2[i,0],'o',color='green')
    
  plt.title(time_list[i])

ani = matplotlib.animation.FuncAnimation(fig, update, frames=numArray, repeat=False)
plt.show()