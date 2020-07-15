import numpy as np
import matplotlib.pyplot as plt
import json

import tools as tl

# this file creates a pass map for each player

# would like to create lists of the time ordered events, individual passing events, 


with open('7298.json') as f:
    data = json.load(f)
    
pass_items = []
player_list = [] 
player_name_list = []
for i in range(len(data)):
    for key,value in data[i]['type'].items():
        if value == 'Pass':
            pass_items.append(data[i])
            if data[i]['player']['id'] not in player_list:
                player_list.append(data[i]['player']['id'])
                player_name_list.append([data[i]['player']['name'],data[i]['position']['name'],data[i]['team']['name']])

print(data[100])

pass_axes = []
X1 = np.zeros((len(pass_items),2))
X2 = np.zeros((len(pass_items),2)) 
Y1 = np.zeros((len(pass_items),2))  
Y2 = np.zeros((len(pass_items),2))

for ii in range(1):
    fig=plt.figure()
    tl.get_pitch()

    for i in range(len(pass_items)):
        pass_axes.append([pass_items[i]['location'],pass_items[i]['pass']['end_location']])
        X1[i] = [pass_axes[i][0][0],pass_items[i]['player']['id']]
        Y1[i] = [pass_axes[i][0][1],pass_items[i]['player']['id']]
        X2[i] = [pass_axes[i][1][0],pass_items[i]['player']['id']]
        Y2[i] = [pass_axes[i][1][1],pass_items[i]['player']['id']]

        if X1[i,1] == player_list[ii]:
            if 'outcome' in pass_items[i]['pass']:
                plt.plot([X1[i,0],X2[i,0]],[Y1[i,0],Y2[i,0]],color='red')
                plt.plot(X2[i,0],Y2[i,0],'X',color='red')
            else:
                plt.plot([X1[i,0],X2[i,0]],[Y1[i,0],Y2[i,0]],color='green')
                plt.plot(X2[i,0],Y2[i,0],'o',color='green')
            

    plt.title(player_name_list[ii][0]+' - '+str(player_name_list[ii][1])+' - '+str(player_name_list[ii][2]) )

plt.show()
