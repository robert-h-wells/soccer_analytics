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

  for i in range(len(match_data)):
    if match_data[i]['home_team']['home_team_name'] == 'Arsenal':
      print(i,match_data[i]['match_id'])
      copyfile('','game_data/')
    elif match_data[i]['away_team']['away_team_name'] == 'Arsenal':
      print(i,match_data[i]['match_id'])


  with open('game_data/3749052.json') as f:
    data = json.load(f)

  with open('game_data/3749079.json') as f:
    data2 = json.load(f)

  data.extend(data2)


  # find data ranges of possession for each team and create list of players
  poss_list, player_list = tl.get_poss_player_list(data)

  for i in range(len(player_list)):
    print(player_list[i])

  # create list of each player and event in each possession pathway
  poss_data, poss_name_data = tl.get_poss_data(data,poss_list,player_list)

  # determine pathway points for each possession
  poss_score = tl.get_path_score(data,poss_list)

  # determine player score (sum of pathway score) and number of pathways they are in
  indiv_score, player_in_path = tl.get_indiv_score(player_list,poss_data,poss_score)

  for i in range(len(player_list)):
    print(player_list[i][1],player_list[i][0],indiv_score[i][0],indiv_score[i][1]) 

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
  
  nam = [x[1] for x in player_list]


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



  if 1==0:
    if 1==0:
      # individual score vs number of pathways
      fig, ax = plt.subplots()
      sort_player = [x for x in sorted(zip(indiv_score,nam), reverse=True)]
      plt.plot([x[0] for x,y in sort_player],[x[1] for x,y in sort_player],'.')
      #plt.xticks([x[0] for x,y in sort_player],labels=[y for x,y in sort_player],rotation=70)
      plt.xlabel('Score') ; plt.ylabel('Num Pathways')
      plt.title('Player Score and Number of Pathways Involved ')

    # score of each pathway vs. length of pathway
    fig, ax = plt.subplots(2,1)
    ax[0].plot(path_length,poss_score,'.')
    ax[1].hist(path_length,bins=20)
    ax[0].set_title('Effect of Length of Pathway')
    plt.xlabel('Pathway Length')
    ax[0].set_ylabel('Score')
    ax[1].set_ylabel('Num Occurences')

    # score of each pathways vs. # of players involved
    fig, ax = plt.subplots(2,1)
    ax[0].plot(num_players,poss_score,'.')
    ax[1].hist(num_players,bins=20)
    ax[0].set_title('Effect of Number of Players')
    plt.xlabel('# of Players')
    ax[0].set_ylabel('Score')
    ax[1].set_ylabel('Num Occurences')
  

  # score of each pathway if certain players are in or not

  #plt.show()


  #=============================================================================================================#
  
  # plot the possession by highest scoring pathways
  sort_poss_list = [x for _,x in sorted(zip(poss_score,poss_list), reverse=True)]
  sort_poss_score = sorted(poss_score, reverse=True)

  for ii in range(7,6):
    fig, ax=plt.subplots()
    pl.get_pitch()
    plt.ylim(100, -10)
    pl.plot_pass_path(data,sort_poss_list[ii][0],sort_poss_list[ii][1])

  #plt.gca().invert_yaxis()
  plt.show()
#=========================================================================================================================#


if __name__ == "__main__":
    main()