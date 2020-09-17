#===============================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import json
import seaborn as sns

import tools as tl
import ml_tools as ml
#===============================================================================================#
def draw_pitch(ax):
    # size of the pitch is 120, 80
    #Create figure

    from matplotlib.patches import Arc, Rectangle, ConnectionPatch

    #Pitch Outline & Centre Line
    ax.plot([0,0],[0,80], color="black")
    ax.plot([0,120],[80,80], color="black")
    ax.plot([120,120],[80,0], color="black")
    ax.plot([120,0],[0,0], color="black")
    ax.plot([60,60],[0,80], color="black")

    #Left Penalty Area
    ax.plot([14.6,14.6],[57.8,22.2],color="black")
    ax.plot([0,14.6],[57.8,57.8],color="black")
    ax.plot([0,14.6],[22.2,22.2],color="black")

    #Right Penalty Area
    ax.plot([120,105.4],[57.8,57.8],color="black")
    ax.plot([105.4,105.4],[57.8,22.5],color="black")
    ax.plot([120, 105.4],[22.5,22.5],color="black")

    #Left 6-yard Box
    ax.plot([0,4.9],[48,48],color="black")
    ax.plot([4.9,4.9],[48,32],color="black")
    ax.plot([0,4.9],[32,32],color="black")

    #Right 6-yard Box
    ax.plot([120,115.1],[48,48],color="black")
    ax.plot([115.1,115.1],[48,32],color="black")
    ax.plot([120,115.1],[32,32],color="black")

    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black",fill=False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")

    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    #Prepare Arcs
    # arguments for arc
    # x, y coordinate of centerpoint of arc
    # width, height as arc might not be circle, but oval
    # angle: degree of rotation of the shape, anti-clockwise
    # theta1, theta2, start and end location of arc in degree
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")

    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

#===============================================================================================#
def get_start_map(data):
    "Make a starting X1 map with positions and initials"

    fig, ax = plt.subplots()
    draw_pitch(ax)
    plt.ylim(100, -10)
    plt.title('Starting XI')

    team = []
    team_nam = []
    initials = []

    for i in data['tactics']['lineup']:
        team.append([i['player']['id'],i['position']['id']])
        team_nam.append([i['player']['name'],i['position']['name']])

    print(team_nam)

    # Position data for map
    pos_dat = [ [0,0], # N/A - 0 
        [5,40], # GK - 1
        [22,70], # RB - 2
        [22,55], # RCB - 3
        [22,40], # CB - 4
        [22,25], # LCB - 5
        [22,10], # LB - 6
        [40,70], # RWB - 7
        [40,10], # LWB - 8
        [40,55], # RDM - 9
        [40,40], # CDM - 10
        [40,25], # LDM - 11
        [60,70], # RM - 12
        [60,55], # RCM - 13
        [60,40], # CM - 14
        [60,25], # LCM - 15
        [60,10], # LM - 16
        [80,70], # RW - 17
        [80,55], # RAM - 18
        [80,40], # CAM - 19
        [80,25], # LAM - 20
        [80,10], # LW - 21
        [105,55], # RCF - 22
        [105,40], # ST - 23
        [105,25], # LCF - 24
        [95,40] # SS - 25
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
        initials.append(nam_id)

    plt.ylim(80, 0)
    plt.xlim(0, 120)

    return(initials)
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
    draw_pitch(ax)
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
    draw_pitch(ax)
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
def indiv_pass_map(pass_data,player_list,type_val):
    """
    Pass heat maps with passing arrows if type_val = 1
    Plot showing arrows from starting locations of each pass (completed and non-completed)
    """

    #for ii in range(len(pass_data)):
    for ii in range(1,2):
        fig, ax = plt.subplots()
        draw_pitch(ax)
        plt.ylim(100, -10)

        if type_val == 1:
            for i in range(len(pass_data[ii])):
                # annotate draw an arrow from a current position to pass_end_location
                arrow_style = '->' ; arrow_color = 'blue'

                if pass_data[ii].iloc[i]['pass_outcome_id'] == 9:
                    arrow_style = "-|>" ; arrow_color = 'red'

                ax.annotate("", xy = (pass_data[ii].iloc[i]['pass_end_location'][0], 
                        pass_data[ii].iloc[i]['pass_end_location'][1]), xycoords = 'data',
                        xytext = (pass_data[ii].iloc[i]['location'][0], 
                        pass_data[ii].iloc[i]['location'][1]), textcoords = 'data',
                        arrowprops=dict(arrowstyle=arrow_style,
                        connectionstyle="arc3", color = arrow_color),)      

        x_coord = [i[0] for i in pass_data[ii]["location"]]
        y_coord = [i[1] for i in pass_data[ii]["location"]]

        #shades: give us the heat map we desire
        # n_levels: draw more lines, the larger n, the more blurry it looks
        sns.kdeplot(x_coord, y_coord, shade = "True", color = "green", n_levels = 30)

        plt.title(player_list[ii][1])
        plt.ylim(80, 0)
        plt.xlim(0, 120)

    plt.show()
#===============================================================================================#
def plot_centroids(centroids, ax, weights=None):
    "Plot centroids for K-means algorithm"

    if weights is not None:
        centroids = centroids[weights > weights.max() / 10]

    ax.scatter(centroids[:, 0], centroids[:, 1],
                marker='d',s=24,linewidths=2,color='darkorange')

                #marker='d', s=16, linewidths=12,
                #color=cross_color, zorder=11, alpha=1)
#===============================================================================================#
def heat_map(df,player_list,player_pos,touch_cluster):
    "Heat map of all player touches."

    num = 12
    fig, ax = plt.subplots(int(num/3),3)
    fig.set_size_inches(18.0, 10.0)

    for ii in range(num): # 11
        if ii >= int(num*2/3):
            val1 = ii - int(2*num/3)
            val2 = 2
        elif ii >= int(num/3):
            val1 = ii - int(num/3)
            val2 = 1
        else:
            val1 = ii
            val2 = 0


        df_player = df[df["player_name"] == player_list[ii][1]]
        df_player = df_player.dropna(subset=["location"])

        # Locations of all events from player
        x_coord = [i[0] for i in df_player["location"]]
        y_coord = [i[1] for i in df_player["location"]]

        draw_pitch(ax[val1,val2])
        plt.ylim(100, -10)

        # Heat map
        sns.kdeplot(x_coord,y_coord,shade = "True",color = "blue",n_levels = 30,ax= ax[val1,val2])

        # Average position
        ax[val1,val2].plot(np.mean(x_coord),np.mean(y_coord),'^',color='red',markersize=14)

        # Plot clusters of position 
        plot_centroids(touch_cluster[ii],ax[val1,val2])
        
        ax[val1,val2].set_title(player_list[ii][1])
        ax[val1,val2].set_ylim(80, 0)
        ax[val1,val2].set_xlim(0, 120)
            
    plt.tight_layout(pad=0.5, w_pad=3.0, h_pad=0.5)
    plt.suptitle('Heat Map for Touches')
    fig.delaxes(ax[3][2])
#===============================================================================================#
def team_heat_map(player_pos,initials):
    # Map of all players average positions

    fig, ax = plt.subplots()
    draw_pitch(ax)
    plt.ylim(100, -10)
    plt.title('Starting XI Heat Map')

    for ii in range(11): # 11
        X1 = player_pos[ii][0]
        Y1 = player_pos[ii][1]
        plt.plot(X1,Y1,'o',color='red',markersize=20)
        plt.text(X1-3.5,Y1+2,initials[ii],fontsize=14)

        plt.ylim(80, 0)
        plt.xlim(0, 120)

#===============================================================================================#
def pass_network(pass_data,player_list,player_pos,pass_cluster):
    """
    More complex version of indiv_pass_map. Will include clustering to find multiple average
    positions of areas where passes began.
    """

    num = 12
    fig, ax = plt.subplots(int(num/3),3)
    fig.set_size_inches(18.0, 10.0)

    for ii in range(num):
        if ii >= int(num*2/3):
            val1 = ii - int(2*num/3)
            val2 = 2
        elif ii >= int(num/3):
            val1 = ii - int(num/3)
            val2 = 1
        else:
            val1 = ii
            val2 = 0

        draw_pitch(ax[val1,val2])
        plt.ylim(100, -10)

        #for i in range(len(pass_data[ii])):
        #    plt.plot(pass_data[ii].iloc[i]['location'][0], pass_data[ii].iloc[i]['location'][1],
        #        'o',color='blue')

        x_coord = [i[0] for i in pass_data[ii]["location"]]
        y_coord = [i[1] for i in pass_data[ii]["location"]]

        # Heat Map of Passing
        sns.kdeplot(x_coord,y_coord,shade = "True",color = "green",n_levels = 30,ax= ax[val1,val2])

        # Average position
        ax[val1,val2].plot(np.mean(x_coord),np.mean(y_coord),'^',color='red',markersize=14)

        # Plot clusters
        plot_centroids(pass_cluster[ii],ax[val1,val2])

        ax[val1,val2].set_title(player_list[ii][1])
        ax[val1,val2].set_ylim(80, 0)
        ax[val1,val2].set_xlim(0, 120)

    plt.tight_layout(pad=0.5, w_pad=3.0, h_pad=0.5)
    plt.suptitle('Heat Map for Passes')
    fig.delaxes(ax[3][2])
#===============================================================================================#
def pass_map(pass_data_recip,player_list,player_pos,initials,n_connect):

    # Need to decide if i want to show connections based on median val or based on n_connect

    mean_val = round(np.median(list([y[0] for x in pass_data_recip for y in x])))
    max_val = int(np.max(list([y[0] for x in pass_data_recip for y in x])))

    fig, ax = plt.subplots()
    fig.set_size_inches(18.0, 10.0)
    draw_pitch(ax)
    plt.ylim(100, -10)

    for i in range(11):

        list_val = [j[0] for j in pass_data_recip[i]]
        check_list = [j for j in pass_data_recip[i]]
        sort_list_val = sorted(check_list, key=lambda x:x[0],reverse=True)

        #fig, ax = plt.subplots()
        #draw_pitch(ax)
        #plt.ylim(100, -10)

        for j in range(len(player_pos)-1):

            X1 = player_pos[j][0]
            Y1 = player_pos[j][1]

            plt.plot(X1,Y1,'o',color='red',markersize=20)
            plt.text(X1-1,Y1,initials[j],fontsize=14)

        # Number of connections to find
        for j in range(len(pass_data_recip[i])):
            player_list_nam = list(jj[1] for jj in player_list[:11])

            if pass_data_recip[i][j][1] in player_list_nam:
                index_val = player_list_nam.index(pass_data_recip[i][j][1])

                if pass_data_recip[i][j][0] > mean_val: 

                    X1 = player_pos[index_val][0]
                    Y1 = player_pos[index_val][1]

                    # Need to make linewidth's more exagerrated, hard to tell
                    gray_map = plt.cm.gray
                    norm_val = (list_val[j]-mean_val)/(max_val-mean_val)
                    ax.annotate("", xy = (X1,Y1),xycoords = 'data',xytext = (player_pos[i][0], 
                                    player_pos[i][1]), textcoords = 'data',
                                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.5',
                                    linewidth=8*norm_val,
                                    connectionstyle="arc3",color = gray_map(1.0-norm_val)),)  # color = 'blue'

        plt.title('Pass Map')
        plt.ylim(80, 0)
        plt.xlim(0, 120)

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