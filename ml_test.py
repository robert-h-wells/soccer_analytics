import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation
from sklearn.pipeline import Pipeline
from scipy.interpolate import griddata

import pass_paths as mn
import tools as tl
import plots as pl

#=============================================================================================================#
def ml_run(df,val_data,percent_poss_score,list_data,nam):

    # Unpack data from pass_paths
    values_length, values_num_players = val_data
    poss_list, player_list = list_data

    sort_length = sorted(set(df['Path_length']))
    sort_num_players = sorted(set(df['Num_players']))
    sort_score = sorted(set(df['Score']))

    event_nam = ['Dribble','Shot','Dribbled_past','Carry']


    # Make plots of the important attributes
    if 1==1:

        if 1==0:  # Make 2 plots

            # score of each pathway vs. length of pathway 
            plot_data = [[],[],[]]
            plot_data[0] = ([[x[0] for x in values_length],[x[1] for x in values_length],
                            [x[2] for x in values_length]])
            plot_data[1] = df['Path_length']
            plot_data[2] = df['Score']
            title = ['Effect of Pathway Length']
            xlabel = ['Path Length','Path Length','Score']
            ylabel = ['Score','Num Occurences','Num Occurences']

            pl.get_ndim_plots([1,3],[4,1,1],plot_data,title,xlabel,ylabel)

            
            # score of each pathways vs. # of players involved
            plot_data = [[],[]]
            plot_data[0] = ([[x[0] for x in values_num_players],[x[1] for x in values_num_players],
                            [x[2] for x in values_num_players]])
            plot_data[1] = df['Num_players'] 
            title = ['Effect of Number of Players']
            xlabel = ['Num Players','Num Players']
            ylabel = ['Score','Num Occurences']

            pl.get_ndim_plots([2,1],[4,1],plot_data,title,xlabel,ylabel)
    

        # want to see how groups of players affect important attributes :: TO-DO IMPROVE
        if 1 == 0:

            val1 = nam[9]
            val2 = nam[10]
            val3 = nam[2]
            val4 = nam[3]

            mult_dat = np.zeros((len(df['Score']),2))
            for i in range(len(df['Score'])):
                if df[val1][i] == 1 and df[val2][i] == 1:
                    mult_dat[i,0] = 1
                else:
                    mult_dat[i,0] = 0

                if df[val3][i] == 1 and df[val4][i] == 1:
                    mult_dat[i,1] = 1
                else:
                    mult_dat[i,1] = 0

            title = ['Henry Bergkmap','Kolo Campbell']
            for i in range(2):
                fig, ax = plt.subplots(1,3)
                ax[0].scatter(df['Path_length'],df['Score'],c=mult_dat[:,i])
                ax[0].set_xlabel('Path Length') ; ax[0].set_ylabel('Score')
                ax[1].scatter(df['Num_players'],df['Score'],c=mult_dat[:,i])
                ax[1].set_title(title[i])
                ax[1].set_xlabel('Num Players') ; ax[1].set_ylabel('Score')
                ax[2].scatter(df['Num_players'],df['Path_length'],c=mult_dat[:,i])
                ax[2].set_xlabel('Num Players') ; ax[2].set_ylabel('Path Length')
                plt.legend()


        if 1==0: 
        # Contour plot of possesion points based on pathway length and num players
        # For each pathway length and num players a percentage of the specific pathway
        # points are determined.

            for val in sort_score:
                data = [i for i in percent_poss_score if i[2] == val]
                if len(data) > 1:
                    xval = np.array([i[0] for i in data])
                    yval = np.array([i[1] for i in data])
                    zval = np.array([i[-1] for i in data])

                    fig, ax = plt.subplots()
                    xi = np.linspace(min(xval),max(xval),np.shape(xval)[0])
                    yi = np.linspace(min(yval),max(yval),np.shape(yval)[0])
                    zi = griddata((xval,yval), zval, (xi[None,:], yi[:,None]), method='nearest' )

                    im = plt.contour(xi,yi,zi,5,linewidths=0.5,colors='k')
                    im = plt.contourf(xi,yi,zi,5,cmap='RdGy')
                    plt.xlabel('Path Length')
                    plt.ylabel('Num Players')
                    plt.title('Pathway Score: '+str(val))

                    fig.colorbar(im)

        # score of each pathway if certain players are in or not      
        if 1==0:

            #for i in range(len(nam)):
            for i in range(5):

                # FOR SCATTER, alpha = 0.1 for easier visualization 
                plot_data = [[],[],[]]

                plot_data[0] = [df['Path_length'],df['Score'],df[nam[i]]]
                plot_data[1] = [df['Num_players'],df['Score'],df[nam[i]]]
                plot_data[2] = [df['Num_players'],df['Path_length'],df[nam[i]]]

                title = [nam[i]] 
                xlabel = ['Path Length','Num Players','Num Players']
                ylabel = ['Score','Score','Path Length']
                pl.get_ndim_plots([1,3],[3,3,3,],plot_data,title,xlabel,ylabel)

        # score based on events in pathway
        if 1==0:

            for i in range(len(event_nam)):

                title = [event_nam[i]]
                plot_data = [[],[],[]]
                xlabel = ['Path Length','Num Players','Num Players']
                ylabel = ['Score','Score','Path Length']

                plot_data[0] = [df['Path_length'],df['Score'],df[event_nam[i]]]
                plot_data[1] = [df['Num_players'],df['Score'],df[event_nam[i]]]
                plot_data[2] = [df['Num_players'],df['Path_length'],df[event_nam[i]]]
                
                pl.get_ndim_plots([1,3],[3,3,3,],plot_data,title,xlabel,ylabel)

        # scored based on beginning position of pathway
        if 1==1:
            for i in range(1,5):
                x = [j for j, e in enumerate(df['Start_val']) if e == i]
                x3 = [df['Score'][i] for i in x]
                fig, ax = plt.subplots()
                plt.hist(x3)
                plt.title('Starting Pathway Value '+str(i))     


        if 1==0:  # this is pretty boring atm
            fig, ax = plt.subplots()
            im = plt.scatter(df['Path_length'],df['Num_players'],c=df['Score'])
            fig.colorbar(im)
            plt.legend()
            plt.xlabel('Path length')
            plt.ylabel('Num of Players')
            plt.title('')
    
    plt.show()
#=============================================================================================================#

# NOW NEED TO WORK ON REGRESSION, CATEGORIES FOR EACH PATHWAY FROM BOOK EXAMPLES

#=============================================================================================================#