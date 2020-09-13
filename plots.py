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
def get_start_map(data):
    "Make a starting X1 map with positions and initials"

    fig, ax = plt.subplots()
    get_pitch()
    plt.ylim(100, -10)
    plt.title('Starting XI')

    team = []
    team_nam = []

    for i in data['tactics']['lineup']:
        team.append([i['player']['id'],i['position']['id']])
        team_nam.append([i['player']['name'],i['position']['name']])

    print(team_nam)

    # Position data for map
    pos_dat = [ [0,0], # N/A - 0 
        [5,45], # GK - 1
        [22,80], # RB - 2
        [22,60], # RCB - 3
        [22,45], # CB - 4
        [22,30], # LCB - 5
        [22,10], # LB - 6
        [44,80], # RWB - 7
        [44,10], # LWB - 8
        [44,60], # RDM - 9
        [44,45], # CDM - 10
        [44,30], # LDM - 11
        [65,80], # RM - 12
        [65,60], # RCM - 13
        [65,45], # CM - 14
        [65,30], # LCM - 15
        [65,10], # LM - 16
        [82,80], # RW - 17
        [82,60], # RAM - 18
        [82,45], # CAM - 19
        [82,30], # LAM - 20
        [82,10], # LW - 21
        [105,60], # RCF - 22
        [105,45], # ST - 23
        [105,30], # LCF - 24
        [95,45] # SS - 25
    ]

    for i,j in zip(team,team_nam):

        try:
            nam_id = [list(j[0].split(' ')[0]),list(j[0].split(' ')[-1])]
            nam_id = str(nam_id[0][0])+str(nam_id[1][0])
        except:
            nam_id = [list(j[0].split(' ')[0]),list(j[0].split(' ')[1])]
            nam_id = str(nam_id[0][0])+str(nam_id[1][0])

        X1 = pos_dat[i[1]][0]
        Y1 = pos_dat[i[1]][1]
        ax.plot(X1,Y1,'o',markersize=20,color='red')
        plt.text(X1-3.5,Y1+2,nam_id,fontsize=14)

    plt.show()
#===============================================================================================#
def get_path_pos_plot(path_start_val):
    " Contour plot for starting pathway positions (x and y) "

    from scipy.interpolate import griddata

    x_vals = [j[0] for j in path_start_val]
    y_vals = [j[1] for j in path_start_val]

    x_percent = []
    y_percent = []

    for j in range(1,5):
        x_percent.append( len([i for i in x_vals if i == j])/len(x_vals) )
        y_percent.append( len([i for i in y_vals if i == j])/len(y_vals) )

    fig, ax = plt.subplots()
    get_pitch()
    plt.ylim(100, -10)
    plt.title('Beginning Positions')

    xi = [0.0,25.0,35.0,55.0,65.0,85.0,95.0,115.0,125.0,130.0]
    yi = [0.0,5.0,15.0,25.0,35.0,45.0,55.0,65.0,75.0,85.0,90.0]
    X, Y = np.meshgrid(xi,yi)
    Z = np.zeros((np.shape(X)))
    Z[:,:2] = x_percent[0]
    Z[:,2:5] = x_percent[1]
    Z[:,5:7] = x_percent[2]
    Z[:,7:] = x_percent[3]

    #im = plt.contour(X,Y,Z,2,linewidths=0.5,colors='k')
    im = plt.contourf(X,Y,Z,4,cmap='RdGy')
    fig.colorbar(im)
    #plt.show()


    fig, ax = plt.subplots()
    get_pitch()
    plt.ylim(100, -10)
    plt.title('Beginning Positions')

    xi = [0.0,25.0,35.0,55.0,65.0,85.0,95.0,115.0,125.0,130.0]
    yi = [0.0,5.0,15.0,25.0,35.0,45.0,55.0,65.0,75.0,85.0,90.0]
    X, Y = np.meshgrid(xi,yi)
    Z = np.zeros((np.shape(X)))
    Z[:3,:] = y_percent[0]
    Z[3:5,:] = y_percent[1]
    Z[5:7,:] = y_percent[2]
    Z[8:,:] = y_percent[3]


    #im = plt.contour(X,Y,Z,2,linewidths=0.5,colors='k')
    im = plt.contourf(X,Y,Z,3,cmap='RdGy')
    fig.colorbar(im)
    plt.show()

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