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

from shutil import copyfile

import tools as tl
import plots as pl
#=========================================================================================================================#

def main():
  # data contains json information 
  # poss_list contains start and end data endices for each possesion  (focusing on Arsenal) 7/16
  # poss_data/poss_name_data gives the id/name of each player and event type for paths 

  with open('game_data/44.json') as f:
    match_data = json.load(f)

  #if files have not been copied to correct directory
  if 1==0:
    for i in range(len(match_data)):
      if match_data[i]['home_team']['home_team_name'] == 'Arsenal':
        src = str('../../../Downloads/open-data-master/open-data-master/data/events/'+str(match_data[i]['match_id'])+'.json')
        dst = str('game_data/'+str(match_data[i]['match_id'])+'.json')
        copyfile(src,dst)
      elif match_data[i]['away_team']['away_team_name'] == 'Arsenal':
        src = str('../../../Downloads/open-data-master/open-data-master/data/events/'+str(match_data[i]['match_id'])+'.json')
        dst = str('game_data/'+str(match_data[i]['match_id'])+'.json')
        copyfile(src,dst)

  data = []
  for i in range(len(match_data)):
  #for i in range(2):
    with open(str('game_data/'+str(match_data[i]['match_id'])+'.json')) as f:
      data2= json.load(f)
      f.close()

    data.extend(data2)


  # find data ranges of possession for each team and create list of players
  poss_list, player_list = tl.get_poss_player_list(data)

  print('Number of games',len(match_data))
  print('Number of players',len(player_list))
  print(player_list)

  for i in range(len(player_list)):
    print(i,player_list[i])

  # create list of each player and event in each possession pathway
  poss_data, poss_name_data = tl.get_poss_data(data,poss_list,player_list)

  # determine pathway points for each possession
  poss_score = tl.get_path_score(data,poss_list)

  # determine player score (sum of pathway score) and number of pathways they are in
  indiv_score, player_in_path = tl.get_indiv_score(player_list,poss_data,poss_score)

  #for i in range(len(player_list)):
    #print(player_list[i][1],player_list[i][0],indiv_score[i][0],indiv_score[i][1]) 

  #=============================================================================================================#

  ## use techniques of machine learning to find the features that make the highest scoring possession pathways ##
  # sort by length, number of players, etc.

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
  print('Shape',np.shape(total_data),np.shape(player_in_path))
  
  nam = [x[1] for x in player_list]
  print(nam)

  #====== Machine Learning tutorial ======#
  if 1==0:

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



  # Examine the data
  if 1==1:
    if 1==0:
      # individual score vs number of pathways
      fig, ax = plt.subplots()
      sort_player = [x for x in sorted(zip(indiv_score,nam), reverse=True)]
      plt.plot([x[0] for x,y in sort_player],[x[1] for x,y in sort_player],'.')
      #plt.xticks([x[0] for x,y in sort_player],labels=[y for x,y in sort_player],rotation=70)
      plt.xlabel('Score') ; plt.ylabel('Num Pathways')
      plt.title('Player Score and Number of Pathways Involved ')

      # score of each pathway vs. length of pathway
      fig, ax = plt.subplots(1,3)
      ax[0].plot(path_length,poss_score,'.')
      ax[1].hist(path_length,bins=30)
      ax[2].hist(poss_score,bins=20)
      ax[2].set_xlabel('Score')
      ax[0].set_title('Effect of Length of Pathway')
      ax[1].set_xlabel('Pathway Length')
      ax[0].set_ylabel('Score')
      ax[1].set_ylabel('Num Occurences')

      # score of each pathways vs. # of players involved
      fig, ax = plt.subplots(2,1)
      ax[0].plot(num_players,poss_score,'.')
      ax[1].hist(num_players,bins=10)
      ax[0].set_title('Effect of Number of Players')
      plt.xlabel('# of Players')
      ax[0].set_ylabel('Score')
      ax[1].set_ylabel('Num Occurences')


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

    ### NEED TO MAKE THE SCATTER PLOTS EXTRAPOLATED GRIDS AND : HEAT MAPS OF POINT PERCENTAGES BASED ON POSITION ##

    sort_score = sorted(set(poss_score))
    percent_poss_score = np.zeros(len(poss_score))

    if 1==1:
      #for j in range(len(path_length)):

      #  check_poss = np.zeros(len(sort_score))
      #  for k in range(len(sort_score)):
      #    if poss_score[j] == sort_score[k]:
      #      check_poss[k] += 1

      #  for jj in range(j+1,len(path_length)):
      #    if path_length[jj] == path_length[j] and num_players[jj] == num_players[j]:
      #      for k in range(len(sort_score)):
      #        if poss_score[j] == sort_score[k]:
      #          check_poss[k] += 1

      #  percent_poss_score[j] = check_poss

      for val in range(len(sort_score)):
        for j in range(len(path_length)):

          check_poss = 0 ; check_others = 0
          if poss_score[j] == sort_score[val]:
            check_poss += 1

            for jj in range(len(path_length)):
              if jj != j:
                if path_length[jj] == path_length[j] and num_players[jj] == num_players[j]:
                  if poss_score[jj] == sort_score[val]:
                    check_poss += 1
                  else:
                    check_others += 1

          if check_poss == 0:
            percent_poss_score[j] = 0
          else:
            percent_poss_score[j] = check_poss / (check_poss+check_others)
            #print(percent_poss_score[j],check_others)
            #if check_others != 0:
            #  print('check others',check_others)

        #print(percent_poss_score)
        fig, ax = plt.subplots()
        xi = np.linspace(min(path_length),max(path_length),np.size(path_length))
        yi = np.linspace(min(num_players),max(num_players),np.size(num_players))
        zi = griddata((path_length,num_players), percent_poss_score, (xi[None,:], yi[:,None]), method='nearest' )

        im = plt.contour(xi,yi,zi,5,linewidths=0.5,colors='k')
        im = plt.contourf(xi,yi,zi,5,cmap='RdGy')

        fig.colorbar(im) # draw colorbar
        #bars.set_label(title[3],fontweight='bold')


    if 1==0:

      sort_length = sorted(set(path_length))
      sort_num_players = sorted(set(num_players))
      sort_score = sorted(set(poss_score))

      for i in range(len(sort_score)):
      #for i in range(9,10):

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
#=========================================================================================================================#


if __name__ == "__main__":
    main()