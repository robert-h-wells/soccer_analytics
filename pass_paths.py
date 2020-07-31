#=========================================================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import json
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from itertools import chain
from scipy.interpolate import griddata
from collections import Counter

from shutil import copyfile

import tools as tl
import plots as pl

# TO-DO LIST ::
  # 2 messy parts to clean up and 1 part that can possibly be made more efficiently (7/29)

#=========================================================================================================================#

def main():
  """
  data contains json information 
  poss_list contains start and end data endices for each possesion  (focusing on Arsenal) 7/16
  poss_data/poss_name_data gives the id/name of each player and event type for paths
  """

  with open('game_data/44.json') as f:
    match_data = json.load(f)

  #if files have not been copied to correct directory
  if 1==0:
    tl.copy_files_tools(match_data)

  # read in game file data
  data = []
  for i in range(len(match_data)):
    with open(str('game_data/'+str(match_data[i]['match_id'])+'.json')) as f:
      data2= json.load(f)
      f.close()

    data.extend(data2)


  # find data ranges of possession for each team and create list of players
  poss_list, player_list = tl.get_poss_player_list(data)
  print('Number of games',len(match_data))
  print('Number of players',len(player_list))

  for i in range(len(player_list)):
    print(i,player_list[i][1])

  # create list of each player and event in each possession pathway
  poss_data, poss_name_data = tl.get_poss_data(data,poss_list,player_list)

  # determine pathway points for each possession
  poss_score = tl.get_path_score(data,poss_list)

  # determine player score (sum of pathway score) and number of pathways they are in
  indiv_score, player_in_path = tl.get_indiv_score(player_list,poss_data,poss_score)


  #==== sort data by length, number of players, etc. ====#

  # find the length of each pathway
  path_length = np.zeros((len(poss_score)))
  for i in range(len(poss_score)):
    path_length[i] = len([x[1] for x in poss_data[i]])

  # number of unique players in each pathway
  num_players = np.zeros((len(poss_score)))
  for i in range(len(poss_score)):
    num_players[i] = len(set([x[0] for x in poss_data[i]]))

  # score, length of path, number of players, is player present
  total_data_ = [path_length,num_players,*([i for i in player_in_path])]
  total_data = np.transpose(total_data_)
  
  # list of player names
  nam = [x[1] for x in player_list]

  #================= Examine the data to find important attributes ==================#
  sort_length = sorted(set(path_length))
  sort_num_players = sorted(set(num_players))
  sort_score = sorted(set(poss_score))

  # determine the degeneracy of combinations of the 3 important attributes
  # length vs score, num players vs score, length and num players vs score
  values_length = []
  values_num_players = []
  values_all = []
  values_total = []

  # probably a better way to determine this !!!! TO DO LIST
  for i in sort_length:
    for j in sort_num_players:

      counts_total = 0

      for k in sort_score:
        
        counts_length = 0 
        counts_players = 0
        counts_all = 0

        for ii in range(len(poss_score)):

          # same length gives same score
          if path_length[ii] == i and poss_score[ii] == k:
            counts_length += 1

          # same num players give same score
          if num_players[ii] == j and poss_score[ii] == k:
            counts_players += 1

          # same length and num players give same score
          if path_length[ii] == i and num_players[ii] == j and poss_score[ii] == k:
            counts_all += 1

          # find number of pathways at length and num players
          if path_length[ii] == i and num_players[ii] == j:
            counts_total += 1

        if counts_length > 0:  values_length.append([i,k,counts_length])
        if counts_players > 0: values_num_players.append([j,k,counts_players])
        if counts_all > 0: values_all.append([i,j,k,counts_all])  

      if counts_total > 0: values_total.append([i,j,counts_total])

  # find the percentage of each possesion point at pathway length and num players
  percent_poss_score = []
  val = 0
  for i in range(len(values_all)):
    if (values_all[i][0] != values_total[val][0] or values_all[i][1] 
      != values_total[val][1]):
      val += 1

    if (values_all[i][0] == values_total[val][0] and values_all[i][1] 
      == values_total[val][1]):
      percent = values_all[i][-1] / values_total[val][-1]
      percent_poss_score.append([values_all[i][0],values_all[i][1],values_all[i][2],percent])
  #==================================================================================#
 

  # Make plots of the important attributes
  if 1==1:

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
  

    # want to see how groups of players affect important attributes :: TO-DO CLEAN UP
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

    if 1==1: 
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


    if 1==0:  # TO-DO: DATA DOES COME OUT NICELY

      for i in range(len(sort_score)):

        #====== Surely there has to be a better way to do this ========#
        # Create a 2d array for percentage of points based on path length and score
        z = np.zeros((len(sort_length),len(sort_num_players),len(sort_score)))

        # loop through original lists
        for j in range(len(path_length)):

          # find which axis value belongs to
          jj_val = 0
          for jj in sort_length:
            kk_val = 0
            for kk in sort_num_players:
              if path_length[j] == jj and num_players[j] == kk:
                val = poss_score[j]

                # Determine which indice the score belongs to
                for ll in range(len(sort_score)):
                  if val == sort_score[ll]:
                    z[jj_val,kk_val,ll] += 1

              else:
                kk_val +=1

            jj_val += 1
         
        z_val = np.zeros((len(sort_length),len(sort_num_players)))
        for j in range(len(sort_length)):
          for k in range(len(sort_num_players)):
            if sum(z[j,k,:]) == 0:
              z_val[j,k] = 0
            else:
              z_val[j,k] = z[j,k,i]/sum(z[j,k,:])


        fig, ax = plt.subplots()
        xi = np.linspace(min(sort_length),max(sort_length),np.size(sort_length))
        yi = np.linspace(min(sort_num_players),max(sort_num_players),np.size(sort_num_players))
        XI, YI = np.meshgrid(xi,yi)

        plt.contour(xi,yi,np.transpose(z_val),5,linewidths=0.5,colors='k')
        plt.contourf(xi,yi,np.transpose(z_val),5,cmap=plt.cm.jet)
        plt.colorbar()
        plt.title('Score '+str(sort_score[i]))


    # score of each pathway if certain players are in or not      
    if 1==0:
      for i in range(len(nam)):
        fig, ax = plt.subplots(1,3)
        ax[0].scatter(path_length,poss_score,c=[x[i+2] for x in total_data])
        ax[0].set_xlabel('Path Length') ; ax[0].set_ylabel('Score')
        ax[1].scatter(num_players,poss_score,c=[x[i+2] for x in total_data])
        #ax[1].contour(num_players,poss_score,[x[i+2] for x in total_data])
        ax[1].set_xlabel('Num Players') ; ax[1].set_ylabel('Score')
        ax[1].set_title(nam[i])
        ax[2].scatter(num_players,path_length,c=[x[i+2] for x in total_data])
        #ax[2].contour(num_player,path_length,[x[i+2] for x in total_data])
        ax[2].set_xlabel('Num Players') ; ax[2].set_ylabel('Path Length')
        plt.legend()


      fig, ax = plt.subplots()
      im = plt.scatter(path_length,num_players,c=poss_score)
      fig.colorbar(im)
      plt.legend()
      plt.xlabel('Path length')
      plt.ylabel('Num of Players')
      plt.title('')


  #=============================================================================================================#
  
  # plot the possession by highest scoring pathways
  sort_poss_list = [x for _,x in sorted(zip(poss_score,poss_list), reverse=True)]
  sort_poss_score = sorted(poss_score, reverse=True)

  for ii in range(10,1):
    fig, ax=plt.subplots()
    pl.get_pitch()
    plt.ylim(100, -10)
    pl.plot_pass_path(data,sort_poss_list[ii][0],sort_poss_list[ii][1])

  #plt.gca().invert_yaxis()
  plt.show()


  #====== Machine Learning tutorial ======#  Will come back to this in the future
  if 1==0:  
    ## use techniques of machine learning to find the features that make 
    ## the highest scoring possession pathways

    # Scaling data
    scaler = StandardScaler()
    scaler.fit(total_data)
    scaled = scaler.transform(total_data)

    # PCA
    names = ['Path Length','Num Players',*nam]
    fig, axes = plt.subplots(5,3,figsize=(12,10))
    ax = axes.ravel()
    for i in range(14):
      _, bins = np.histogram(total_data_[i])
      ax[i].hist(total_data_[i],bins=bins)
      ax[i].set_title(names[i])

    fig.tight_layout()

    pca = PCA(n_components=2)
    pca.fit(scaled)
    X_pca = pca.transform(scaled)
    print(pca.components_)
    plt.matshow(pca.components_)
    plt.colorbar()
    plt.xticks(range(len(names)),labels=names,rotation=70)

    #plt.plot([x[0] for x in X_pca],[x[1] for x in X_pca],'.',c=poss_score)
    fig, ax = plt.subplots()
    im = plt.scatter([x[0] for x in X_pca],[x[1] for x in X_pca],c=poss_score)
    fig.colorbar(im)
    plt.legend()
    plt.gca().set_aspect("equal")
    plt.title('PCA')
#=========================================================================================================================#


if __name__ == "__main__":
    main()