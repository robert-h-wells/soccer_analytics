import numpy as np
import matplotlib.pyplot as plt
import json

#===================================================#
def get_pitch():
    #Pitch Outline & Centre Line
    plt.plot([0,0],[0,90], color="black")
    plt.plot([0,130],[90,90], color="black")
    plt.plot([130,130],[90,0], color="black")
    plt.plot([130,0],[0,0], color="black")
    plt.plot([65,65],[0,90], color="black")

    #Left Penalty Area
    plt.plot([16.5,16.5],[65,25],color="black")
    plt.plot([0,16.5],[65,65],color="black")
    plt.plot([16.5,0],[25,25],color="black")

    #Right Penalty Area
    plt.plot([130,113.5],[65,65],color="black")
    plt.plot([113.5,113.5],[65,25],color="black")
    plt.plot([113.5,130],[25,25],color="black")

    #Left 6-yard Box
    plt.plot([0,5.5],[54,54],color="black")
    plt.plot([5.5,5.5],[54,36],color="black")
    plt.plot([5.5,0.5],[36,36],color="black")

    #Right 6-yard Box
    plt.plot([130,124.5],[54,54],color="black")
    plt.plot([124.5,124.5],[54,36],color="black")
    plt.plot([124.5,130],[36,36],color="black")
#===================================================#


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
                player_name_list.append(data[i]['player']['name'])


pass_axes = []
X1 = np.zeros((len(pass_items),2))
X2 = np.zeros((len(pass_items),2)) 
Y1 = np.zeros((len(pass_items),2))  
Y2 = np.zeros((len(pass_items),2))

for ii in range(10):
    fig=plt.figure()
    get_pitch()

    for i in range(len(pass_items)):
        pass_axes.append([pass_items[i]['location'],pass_items[i]['pass']['end_location']])
        X1[i] = [pass_axes[i][0][0],pass_items[i]['player']['id']]
        Y1[i] = [pass_axes[i][0][1],pass_items[i]['player']['id']]
        X2[i] = [pass_axes[i][1][0],pass_items[i]['player']['id']]
        Y2[i] = [pass_axes[i][1][1],pass_items[i]['player']['id']]

        if X1[i,1] == player_list[ii]:
            if 'outcome' in pass_items[i]['pass']:
                #plt.quiver(X1[i,0],Y1[i,0],X2[i,0]-X1[i,0],Y2[i,0]-Y1[i,0],headwidth=1.5,color='red')
                plt.plot([X1[i,0],X2[i,0]],[Y1[i,0],Y2[i,0]],color='red')
                plt.plot(X2[i,0],Y2[i,0],'X',color='red')
            else:
                #plt.quiver(X1[i,0],Y1[i,0],X2[i,0]-X1[i,0],Y2[i,0]-Y1[i,0],headwidth=1.5)
                plt.plot([X1[i,0],X2[i,0]],[Y1[i,0],Y2[i,0]],color='green')
                plt.plot(X2[i,0],Y2[i,0],'o',color='green')
            

    plt.title(player_name_list[ii])

plt.show()
