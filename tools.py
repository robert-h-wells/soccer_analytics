#===============================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import json

import plots as pl
import ml_tools as ml
#===============================================================================================#
def get_poss_player_list(data):
    # from data, determine start and end data points for each possession pathway 
    # # (just Arsenal for now)
    # determine all players in the full match

    switch = 0
    prev_switch = 1
    prev_poss = data[1]['possession']
    poss_list = []
    player_list = []

    for i in range(len(data)):
        if data[i]['type']['id'] in [19, 35]: # Starting XI and subs        
            if data[i]['type']['id'] == 35:
                if data[i]['team']['name'] == 'Arsenal':
                    #print(data[i]) ; print(i)
                    for i in data[i]['tactics'].get('lineup'):
                        if [i['player']['id'],i['player']['name']] not in player_list:
                            player_list.append([i['player']['id'],i['player']['name']])
            
            elif data[i]['type']['id'] == 19:
                if data[i]['team']['name'] == 'Arsenal':
                    if ([data[i]['substitution']['replacement']['id'],
                        data[i]['substitution']['replacement']['name']] not in player_list):

                        player_list.append([data[i]['substitution']['replacement']['id'], 
                        data[i]['substitution']['replacement']['name']])
        
        elif data[i]['possession'] != data[i-1]['possession']:
            switch += 1
            if data[i-1]['possession_team']['name'] == 'Arsenal':
                poss_list.append([prev_switch,i])

            prev_switch = i

    return(poss_list, player_list)
#===============================================================================================#
def get_poss_data(data,poss_list,player_list):
    """ 
    Create lists of each player and each event that occurs along each pathways.
    Also want to find the average position of each player based on all touches.
    """

    poss_data = []
    poss_name_data = []
    
    for i in range(len(poss_list)):
        poss_data.append([])
        poss_name_data.append([])
        new_list = [] ; new_name_list = []

        for j in range(poss_list[i][0], poss_list[i][1]):
            try:
                # make sure they are arsenal players
                player_val = [x[0] for x in player_list]
                if data[j]['player']['id'] in player_val: 

                    new_list.append([data[j]['player']['id'],data[j]['type']['id']])
                    new_name_list.append([data[j]['player']['name'],data[j]['type']['name']])
            
            except KeyError:
                pass

        poss_data[i] = new_list
        poss_name_data[i] = new_name_list

    return(poss_data, poss_name_data)
#===============================================================================================#
def get_touch_data(df,player_list):
    """ 
    Get average position of each player based on touch.
    Also use K-Means to get cluster position of each player.
    """
 
    player_pos = []
    touch_cluster = []
    for ii in range(len(player_list)):

        df_player = df[df["player_name"] == player_list[ii][1]]
        df_player = df_player.dropna(subset=["location"])

        # Locations of all events from player
        x_coord = [i[0] for i in df_player["location"]]
        y_coord = [i[1] for i in df_player["location"]]

        # Find average of all events
        player_pos.append([np.mean(x_coord),np.mean(y_coord)])

        # K-means to find clusters
        X = list(zip(x_coord,y_coord))
        kmeans = ml.find_cluster(X,[2,6])
        touch_cluster.append(kmeans.cluster_centers_)

    return(player_pos,touch_cluster)
#===============================================================================================#
def get_path_pos(data,poss_list):
    # get the starting position of each pathway and assign value

    path_start_pos = []
    path_start_val = []

    for i in range(len(poss_list)):
        path_start_pos.append(data[poss_list[i][0]]['location'])
        
        # Starting X position
        if path_start_pos[i][0] <= 30:
            val_x = 1
        elif path_start_pos[i][0] <= 60:
            val_x = 2
        elif path_start_pos[i][0] <= 90:
            val_x = 3
        elif path_start_pos[i][0] <= 120:
            val_x = 4
        else:
            print('problem_x')
            print(path_start_pos[i])

        # Starting Y position
        if path_start_pos[i][1] <= 20:
            val_y = 1
        elif path_start_pos[i][1] <= 40:
            val_y = 2
        elif path_start_pos[i][1] <= 60:
            val_y = 3
        elif path_start_pos[i][1] <= 80:
            val_y = 4
        else:
            print('problem_y')
            print(path_start_pos[i])

        path_start_val.append([val_x,val_y])

    return(path_start_pos,path_start_val)
#===============================================================================================#
def get_path_score(data,poss_list):
    # determine result of the possession pathway and give score

    poss_score = len(poss_list)*[None]
    poss_score[0] = 0 ; poss_score[1] = 0

    for i in range(len(poss_list)):

        val = poss_list[i][1]-1

        try:

            if data[val+1]['possession_team']['name'] == 'Arsenal':  # possesion stays
                if data[val+1]['play_pattern']['id'] == 1:    # maintaiend possession 
                    poss_score[i] = 0
                elif data[val+1]['play_pattern']['id'] == 2:  # caused a corner kick
                    poss_score[i] = 3
                elif data[val+1]['play_pattern']['id'] == 3:  # caused a free kick
                    poss_score[i] = 2
                elif data[val+1]['play_pattern']['id'] == 4:  # caused a throw in
                    poss_score[i] = 1
                elif data[val+1]['play_pattern']['id'] == 5:  # something happened
                    poss_score[i] = 0
                elif data[val+1]['play_pattern']['id'] == 7:  # caused a goal kick
                    poss_score[i] = 1
                elif data[val+1]['play_pattern']['id'] == 8:  # Arsenal keeper got ball
                    poss_score[i] = 0
                elif data[val+1]['play_pattern']['id'] == 9:  # half start
                    poss_score[i] = 0
                elif data[val]['type']['id'] == 21:  # foul won
                    if data[val]['foul_won']['penalty'] == 'True':  # penalty won
                        print('Penalty!!!')
                        poss_score[i] = 5
                    else:                                           # free kick won
                        print('Free kick won')
                        poss_score[i] = 3
                elif data[val+1]['pass']['outcome']['id'] in [9,74,75,76]: # incomplete pass
                    print('Incomplete pass')
                    poss_score[i] = 0
                
                else:
                    print('====================================')
                    print('NEW TYPE')
                    print('==================================== \n')


            # DETERMINE POINTS WITH END RESULT FOR TURNOVER PATHWAY, NEED MORE NEGATIVE VALUES         
            elif data[val+1]['possession_team']['name'] != 'Arsenal':  # possesion changes

                if (i+1 == len(poss_list)):
                    poss_score[i] = 0
                    print('last possesion')
                    print(data[-1])
                else:
                    poss2 = poss_list[i+1][1]-1 ; poss_val = data[val]['possession']
                    for ii in range(val,poss2):
                        if data[ii]['possession'] == poss_val +2:
                            poss2_val = ii-1
                            break
                    #try:
                    #    if data[poss2_val]['type']['id'] in [16]:  # 21
                    #        print('checks',poss_list[i],data[val]['possession'],data[poss2_val]['possession'],data[poss2_val]['possession']-data[val]['possession'])
                    #        print(data[poss2_val])
                    #        print(data[poss2_val]['play_pattern']) ; print()
                    
                    #except:
                    #    pass

                    check_play = any('play_pattern' in x for x in data[val+1])
                    check_keeper = any('goalkeeper' in x for x in data[val])

                    if check_keeper == True:
                        if data[val]['goalkeeper']['type']['id'] in [26, 27, 28, 29, 30, 31, 32, 33, 34]:
                            if data[val]['goalkeeper']['type']['id'] == 26: # goal scored
                                poss_score[i] = 10
                            elif data[val]['goalkeeper']['type']['id'] == 27: # sweeper keeper
                                poss_score[i] = 1
                            elif data[val]['goalkeeper']['type']['id'] == 28: # penalty conceded
                                poss_score[i] = 8
                            elif data[val]['goalkeeper']['type']['id'] == 29: # penalty saved
                                poss_score[i] = 5
                            elif data[val]['goalkeeper']['type']['id'] == 30: # keeper punch
                                poss_score[i] = 3
                            elif data[val]['goalkeeper']['type']['id'] == 31: # save from a non-shot
                                poss_score[i] = 1
                            elif data[val]['goalkeeper']['type']['id'] == 32: # shot faced
                                poss_score[i] = 2
                            elif data[val]['goalkeeper']['type']['id'] == 33: # shot saved
                                poss_score[i] = 4
                            elif data[val]['goalkeeper']['type']['id'] == 34: # keeper smother
                                poss_score[i] = 2
                        else: 
                            print('Here is something weird')


                    elif check_play == True:
                        if data[val+1]['play_pattern']['id'] == 1:  # open play, gave ball away
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -7
                            else:
                                poss_score[i] = -2
                        elif data[val+1]['play_pattern']['id'] == 2:  # caused a corner kick 
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -8
                            else:
                                poss_score[i] = -3
                        elif data[val+1]['play_pattern']['id'] == 3:  # caused a free kick
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -8
                            else:
                                poss_score[i] = -3
                        elif data[val+1]['play_pattern']['id'] == 4:  # caused a throw in
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -6
                            else:
                                poss_score[i] = -1
                        elif data[val+1]['play_pattern']['id'] == 5:  # other
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -6
                            else:
                                poss_score[i] = -1
                        elif data[val+1]['play_pattern']['id'] == 6:  # caused counter
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -7
                            else:
                                poss_score[i] = -2
                        elif data[val+1]['play_pattern']['id'] == 7:  # caused a goal kick
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -6
                            else:
                                poss_score[i] = -1
                        elif data[val+1]['play_pattern']['id'] == 8:  # other keeper got ball
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -6
                            else:
                                poss_score[i] = -1
                        elif data[val]['play_pattern']['id'] == 8:  # keeper got the ball but didn't keep possesion
                            if data[poss2_val]['type']['id'] in [16,21]:
                                poss_score[i] = -5
                            else:
                                poss_score[i] = 0

                        elif data[val+1]['play_pattern']['id'] == 9: # from kick off
                            poss_score[i] = 0
                    
                        else:
                            print('**************************************************************')
                            print('did not get a score')
                            print('val-1',data[val-1]) ; print('')
                            print('val',data[val]) ; print('')
                            print('val+1',data[val+1])
                            print('**************************************************************')

                    else:
                        if data[val]['type']['id'] == 18:  # kickoff from halftime
                            poss_score[i] = 0
                    
                        elif data[val+1]['type']['id'] == 23:
                            print('SOMETHING')
                            poss_score[i] = 1

            

                        else:
                            print('NEW NEW')
                            print('')

            else:
                print('WTF')

        except KeyError as e:
            print('========================================================')
            print(str(e))
            print('KeyError')
            print(data[val+1]['possession_team']['name'])
            print(data[val+1]['play_pattern']['id'])
            print('val-1',data[val-1]) ; print('')
            print('val',data[val])
            print('')
            print('val+1',data[val+1])
            print('========================================================')

    return(poss_score)
#===============================================================================================#
def get_indiv_score(player_list,poss_data,poss_score):
    # sum of pathway points = individual score, finds number of pathways involved 
    # returns 1 or 0 for each pathway if player is in pathway

    # initialize list size
    indiv_score = []
    player_in_path = [[0 for i in range(len(poss_data))] for j in range(len(player_list))]
    player_in_path_check = [[0 for i in range(len(poss_data))] for j in range(len(player_list))]

    event_list = [14,16,39,43]
    event_in_path = [[0 for i in range(len(poss_data))] for j in range(len(event_list))]

    for val, (id_val, type_val) in enumerate(player_list):

        score = 0
        num_events = 0
        
        # check each pathway for players included 
        for i in range(len(poss_data)):

            # player in pathway
            player_set = set([x[0] for x in poss_data[i]])
            player_val = id_val in player_set
            palyer_val = int(player_val == True)
            player_in_path[val][i] = player_val

            # give pathway score to players in pathway
            if player_val == 1:
                score += poss_score[i]
                num_events += 1
                player_in_path[val][i] = 1

        indiv_score.append([score,num_events])

    # determine what events happen in each pathway
    for val, id_val in enumerate(event_list):

        for i in range(len(poss_data)):
            event_set = set([x[1] for x in poss_data[i]])
            event_val = id_val in event_set
            event_val = int(event_val == True)
            event_in_path[val][i] = event_val

    return(indiv_score,player_in_path,event_in_path)
#===============================================================================================#
def get_path_info(path_length,num_players,poss_score):
    # input needed
    # poss_score,path_length,num_players

    values_length = []
    values_num_players = []
    values_all = []
    values_total = []

    sort_length = sorted(set(path_length))
    sort_num_players = sorted(set(num_players))
    sort_score = sorted(set(poss_score))

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

    return(values_length,values_num_players,values_all,values_total)
#===============================================================================================#
def get_percent_poss_score(values_all,values_total):

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

    return(percent_poss_score)    
#===============================================================================================#
def get_pass_data(player_list,df):
    """
    Get details of passes from each player. Find recipients of their passes.
    Also use K-Means to determine the passing clusters for the player to get
    a more accurate representation of where their average passing positions occur.
    """

    # Find all events of passing for each player
    pass_data = []
    for i in player_list:
        pass_data.append(df[(df['player_name'] == i[1]) & (df['type_name'] == 'Pass')])

    # Find recipients of each passing event
    pass_data_recip = []
    for i in range(len(pass_data)):
        lister = list(pass_data[i]['pass_recipient_name'])
        val = [lister.count(j) for j in list(set(lister))]
        zip_val = [j for j in zip(val,list(set(lister)))]
        pass_data_recip.append(zip_val)

    # Find centroids of passing through K-Means
    pass_cluster = []
    for ii in range(len(pass_data)):
        lister = list(pass_data[ii]['pass_recipient_name'])

        x_coord = [i[0] for i in pass_data[ii]["location"]] 
        y_coord = [i[1] for i in pass_data[ii]["location"]]

        # K-means to get clusters
        X = list(zip(x_coord,y_coord))
        kmeans = ml.find_cluster(X,[3,5])
        
        # Separate passing data into each cluster
        cluster_data = []
        for j in range(len(kmeans.cluster_centers_)):
            cluster_recip = [list(i) for i in pass_data_recip[ii]]
            for jj in cluster_recip:
                jj[0] = 0

            # Find recipients for data in each cluster
            for k in range(len(kmeans.labels_)):

                if kmeans.labels_[k] == j:
                    for x in cluster_recip:

                        if x[1] == lister[k]:
                            x[0] += 1

            cluster_data.append(cluster_recip)
            
        pass_cluster.append([kmeans.cluster_centers_,cluster_data])

    return(pass_data,pass_data_recip,pass_cluster)
#===============================================================================================#
def cluster_data(pass_data,player_list,player_pos,pass_cluster):

    cluster_pos = [i[0] for i in pass_cluster]
    cluster_recip = [i[1] for i in pass_cluster]

    import itertools
    check = list(itertools.chain(*cluster_recip))
    check2 = list(itertools.chain(*check))
    check3 = list([i[0] for i in check2])
    #mean_val = round(np.median(check3))
    mean_val = 3
    max_val = int(np.max(check3))
    print(mean_val,max_val)

    attack_pos = []
    defense_pos = []

    # Need to get correct data for the special cases
    # 0 and 2 wont work for attack and defense for arrow

    # Find each player position
    for i in range(11):

        if i == 0:  # special case for Lehmann
            attack = sorted(cluster_pos[i], key=lambda x:x[0], reverse=True)
            attack[0] = attack[1]

            defense = attack

        elif i == 2: # Kolo
            attack = sorted(cluster_pos[i], key=lambda x:x[0])
            defense = sorted(cluster_pos[i], key=lambda x:x[0])

        elif i == 3: # Sol
            attack = sorted(cluster_pos[i], key=lambda x:x[0], reverse=True)
            defense = sorted(cluster_pos[i], key=lambda x:x[1])

        elif i == 9: # Bergkamp
            attack = sorted(cluster_pos[i], key=lambda x:x[0], reverse=True)
            defense = sorted(cluster_pos[i], key=lambda x:x[0], reverse=True)
            defense[0] = defense[1]

        else: # sort by x axis
            attack = sorted(cluster_pos[i], key=lambda x:x[0], reverse=True)
            defense = sorted(cluster_pos[i], key=lambda x:x[0])

        attack_pos.append(attack)
        defense_pos.append(defense)


    # Attack Map
    fig, ax = plt.subplots()
    pl.draw_pitch(ax)
    plt.ylim(100, -10)

    for i in range(11):

        X1 = attack_pos[i][0][0]
        Y1 = attack_pos[i][0][1]
        plt.plot(X1,Y1,'o',color='red',markersize=20)
        plt.text(X1-3.5,Y1+2,player_list[i][1],fontsize=8)

        # Plot passing connections
        for j in range(len(cluster_recip[i][0])):
            player_list_nam = list(jj[1] for jj in player_list[:11])

            if cluster_recip[i][0][j][1] in player_list_nam:
                index_val = player_list_nam.index(cluster_recip[i][0][j][1])

                if cluster_recip[i][0][j][0] > mean_val:

                    X2 = attack_pos[index_val][0][0]
                    Y2 = attack_pos[index_val][0][1]

                    # Passing arrow
                    gray_map = plt.cm.gray
                    norm_val = (cluster_recip[i][0][j][0]-mean_val)/(max_val-mean_val)
                    ax.annotate("", xy = (X2,Y2),xycoords = 'data',xytext = (X1, 
                                    Y1), textcoords = 'data',
                                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.5',
                                    linewidth=8*norm_val,
                                    connectionstyle="arc3",color = gray_map(1.0-norm_val)),)

        plt.ylim(80, 0)
        plt.xlim(0, 120)
        plt.title('Attacking Positions')


    # Defensive Map
    fig, ax = plt.subplots()
    pl.draw_pitch(ax)
    plt.ylim(100, -10)

    for i in range(11):  

        X1 = defense_pos[i][0][0]
        Y1 = defense_pos[i][0][1]
        plt.plot(X1,Y1,'o',color='red',markersize=20)
        plt.text(X1-3.5,Y1+2,player_list[i][1],fontsize=8)

        # Plot passing connections
        for j in range(len(cluster_recip[i][0])):
            player_list_nam = list(jj[1] for jj in player_list[:11])

            if cluster_recip[i][0][j][1] in player_list_nam:
                index_val = player_list_nam.index(cluster_recip[i][0][j][1])

                if cluster_recip[i][-1][j][0] > mean_val:

                    X2 = defense_pos[index_val][0][0]
                    Y2 = defense_pos[index_val][0][1]

                    # Passing arrow
                    gray_map = plt.cm.gray
                    norm_val = (cluster_recip[i][-1][j][0]-mean_val)/(max_val-mean_val)
                    ax.annotate("", xy = (X2,Y2),xycoords = 'data',xytext = (X1, 
                                    Y1), textcoords = 'data',
                                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.5',
                                    linewidth=8*norm_val,
                                    connectionstyle="arc3",color = gray_map(1.0-norm_val)),)

        plt.ylim(80, 0)
        plt.xlim(0, 120)
        plt.title('Defensive Positions')

#===============================================================================================#
def copy_files_tools(match_data):
    """ Copy files from source to game_data folder """

    for i in range(len(match_data)):
        if match_data[i]['home_team']['home_team_name'] == 'Arsenal':
            src = (str('../../../Downloads/open-data-master/open-data-master/data/events/'
                    +str(match_data[i]['match_id'])+'.json'))
            dst = str('game_data/'+str(match_data[i]['match_id'])+'.json')
            copyfile(src,dst)
        elif match_data[i]['away_team']['away_team_name'] == 'Arsenal':
            src = (str('../../../Downloads/open-data-master/open-data-master/data/events/'
                    +str(match_data[i]['match_id'])+'.json'))
            dst = str('game_data/'+str(match_data[i]['match_id'])+'.json')
            copyfile(src,dst)
#===============================================================================================#