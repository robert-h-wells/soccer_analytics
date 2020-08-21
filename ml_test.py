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
def ml_run(total_data_,val_data,percent_poss_score,list_data,nam):

    # Unpack data from pass_paths
    path_length, num_players, *_, a,b,c,d, poss_score = total_data_
    total_data = np.transpose(total_data_)
    print(np.shape(total_data))
    values_length, values_num_players = val_data
    poss_list, player_list = list_data

    event_in_path = [a,b,c,d]
    print(np.shape(event_in_path))

    sort_length = sorted(set(path_length))
    sort_num_players = sorted(set(num_players))
    sort_score = sorted(set(poss_score))

    # Make plots of the important attributes
    if 1==0:

        if 1==0:  # Make 2 plots

            # score of each pathway vs. length of pathway 
            plot_data = [[],[],[]]
            plot_data[0] = ([[x[0] for x in values_length],[x[1] for x in values_length],
                            [x[2] for x in values_length]])
            plot_data[1] = path_length
            plot_data[2] = poss_score
            title = ['Effect of Pathway Length']
            xlabel = ['Path Length','Path Length','Score']
            ylabel = ['Score','Num Occurences','Num Occurences']

            pl.get_ndim_plots([1,3],[4,1,1],plot_data,title,xlabel,ylabel)

            
            # score of each pathways vs. # of players involved
            plot_data = [[],[]]

            plot_data[0] = ([[x[0] for x in values_num_players],[x[1] for x in values_num_players],
                            [x[2] for x in values_num_players]])
            plot_data[1] = num_players
            title = ['Effect of Number of Players']
            xlabel = ['Num Players','Num Players']
            ylabel = ['Score','Num Occurences']

            pl.get_ndim_plots([2,1],[4,1],plot_data,title,xlabel,ylabel)
    

        # want to see how groups of players affect important attributes :: TO-DO IMPROVE
        if 1 == 0:
            mult_dat = np.zeros((len(poss_score),2))
            for i in range(len(poss_score)):
                if total_data[i][9] == 1 and total_data[i][10] == 1:
                    mult_dat[i,0] = 1
                else:
                    mult_dat[i,0] = 0

                if total_data[i][2] == 1 and total_data[i][3] == 1:
                    mult_dat[i,1] = 1
                else:
                    mult_dat[i,1] = 0

            title = ['Henry Bergkmap','Kolo Campbell']
            for i in range(2):
                fig, ax = plt.subplots(1,3)
                ax[0].scatter(path_length,poss_score,c=mult_dat[:,i])
                ax[0].set_xlabel('Path Length') ; ax[0].set_ylabel('Score')
                ax[1].scatter(num_players,poss_score,c=mult_dat[:,i])
                ax[1].set_title(title[i])
                ax[1].set_xlabel('Num Players') ; ax[1].set_ylabel('Score')
                ax[2].scatter(num_players,path_length,c=mult_dat[:,i])
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
            for i in range(2):

                # FOR SCATTER, alpha = 0.1 for easier visualization 

                plot_data = [[],[],[]]
                plot_data[0] = [path_length,poss_score,[x[i+2] for x in total_data]]
                plot_data[1] = [num_players,poss_score,[x[i+2] for x in total_data]]
                plot_data[2] = [num_players,path_length,[x[i+2] for x in total_data]]
                title = [nam[i]]
                xlabel = ['Path Length','Num Players','Num Players']
                ylabel = ['Score','Score','Path Length']
                pl.get_ndim_plots([1,3],[3,3,3,],plot_data,title,xlabel,ylabel)

        if 1==1:
            event_nam = ['Dribble','Shot','Dribbled Past','Carry']
            for i in range(4):

                title = [event_nam[i]]
                plot_data = [[],[],[]]
                xlabel = ['Path Length','Num Players','Num Players']
                ylabel = ['Score','Score','Path Length']
                #plot_data[0] = [path_length,poss_score,[x[-5+i] for x in total_data]]
                plot_data[0] = [path_length,poss_score,[x[i+2] for x in total_data]]


                plot_data[1] = [num_players,poss_score,[x[-5+i] for x in total_data]]
                plot_data[2] = [num_players,path_length,[x[-5+i] for x in total_data]]
                pl.get_ndim_plots([1,3],[3,3,3,],plot_data,title,xlabel,ylabel)



        if 1==0:  # this is pretty boring atm
            fig, ax = plt.subplots()
            im = plt.scatter(path_length,num_players,c=poss_score)
            fig.colorbar(im)
            plt.legend()
            plt.xlabel('Path length')
            plt.ylabel('Num of Players')
            plt.title('')
    
    plt.show()
#=============================================================================================================#