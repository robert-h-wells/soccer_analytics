#===============================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import json
#===============================================================================================#
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
#===============================================================================================#
def plot_pass_path(data,start_val,end_val):
    # creates a movie of individual events during a possession sequence

    for i in range(start_val, end_val):

        value = data[i]['type']['name']
        val_id = data[i]['type']['id']
        type_val = 1

        if data[i]['team']['name'] != 'Arsenal':
            value = 'Pressure'
            val_id = 17

        if val_id == 30:  # pass
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
        
        elif val_id in [14, 42]:  # dribble or ball receipt
            X1 = data[i]['location'][0]
            Y1 = data[i]['location'][1]
            plt.plot(X1,Y1,'D',color='blue')

        elif val_id == 16:      # shot
            X1 = data[i]['location'][0]
            Y1 = data[i]['location'][1]
            plt.plot(X1,Y1,'*',color='yellow')

        elif val_id in [4, 17, 22, 39]:   # duel, pressure, foul committed, dribbled past
            type_val = 0
        
        else:
            X1 = data[i]['location'][0]
            Y1 = data[i]['location'][1]
            plt.plot(X1,Y1,'o',color='gray')

        if type_val == 1:
            plt.title(data[i]['timestamp']+'\n '+value+' '+data[i]['player']['name'])
            plt.pause(1.0)

    #plt.gca().invert_yaxis()
#===============================================================================================#
def get_ndim_plots(dim,plot_type,data,title,xlabel,ylabel):  # ,labels
    """
    Make dim[0] x dim[1] plot where plot_type determines the tye of subplot.
    0 - plot, 1 - hist, 2 - scatter, 3 - scatter with color labels, 4 - scatter with color and size
    
    Data is n-dim list which corresponds to number of subplots.
    """
    fig, ax = plt.subplots(dim[0],dim[1])
    
    val = 0
    for x in range(dim[0]):
        for y in range(dim[1]):
            
            if plot_type[val] == 0:  # plot
                print('nope')

            elif plot_type[val] == 1:  # hist
                ax[val].hist(data[val])
                ax[val].set_xlabel(xlabel[val])
                ax[val].set_ylabel(ylabel[val])

            elif plot_type[val] == 2:  # scatter
                ax[val].scatter(data[val][0],data[val][1],alpha=0.5)
                ax[val].set_xlabel(xlabel[val])
                ax[val].set_ylabel(ylabel[val])

            elif plot_type[val] == 3:  # scatter with color labels
                ax[val].scatter(data[val][0],data[val][1],c=data[val][2],alpha=0.5,
                    cmap=plt.get_cmap("jet"))
                ax[val].set_xlabel(xlabel[val])
                ax[val].set_ylabel(ylabel[val])

            elif plot_type[val] == 4:  # scatter with color and size labels
                ax[val].scatter(data[val][0],data[val][1],c=data[val][2],s=data[val][2],
                    alpha=0.5,cmap=plt.get_cmap("jet"))
                ax[val].set_xlabel(xlabel[val])
                ax[val].set_ylabel(ylabel[val])

            val += 1

    plt.suptitle(title[-1])
#===============================================================================================#