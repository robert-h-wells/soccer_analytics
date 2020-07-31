#===============================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import json
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
    # create lists of each player and each even that occurs along each pathways

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
                    # should check  for certain events NOT IN YET

                    new_list.append([data[j]['player']['id'],data[j]['type']['id']])
                    new_name_list.append([data[j]['player']['name'],data[j]['type']['name']])
            except KeyError:
                pass

        poss_data[i] = new_list
        poss_name_data[i] = new_name_list

    return(poss_data, poss_name_data)
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
                        poss_score[i] = -2
                    elif data[val+1]['play_pattern']['id'] == 2:  # caused a corner kick 
                        poss_score[i] = -3
                    elif data[val+1]['play_pattern']['id'] == 3:  # caused a free kick
                        poss_score[i] = -3
                    elif data[val+1]['play_pattern']['id'] == 4:  # caused a throw in
                        poss_score[i] = -1
                    elif data[val+1]['play_pattern']['id'] == 5:  # other
                        poss_score[i] = -1
                    elif data[val+1]['play_pattern']['id'] == 6:  # caused counter
                        poss_score[i] = -2
                    elif data[val+1]['play_pattern']['id'] == 7:  # caused a goal kick
                        poss_score[i] = -1
                    elif data[val+1]['play_pattern']['id'] == 8:  # other keeper got ball
                        poss_score[i] = -1
                    elif data[val]['play_pattern']['id'] == 8:  # keeper got the ball but didn't keep possesion
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

    indiv_score = []
    player_in_path = [[0 for i in range(len(poss_data))] for j in range(len(player_list))]

    for val, (id_val, type_val) in enumerate(player_list):
        score = 0
        num_events = 0
        
        for i in range(len(poss_data)):
            event_val = 0 

            for j in range(len(poss_data[i])):
                if id_val == poss_data[i][j][0]:
                    event_val = 1

            if event_val == 1:
                score += poss_score[i]
                num_events += 1
                player_in_path[val][i] = 1
            elif event_val == 0:
                player_in_path[val][i] = 0

        indiv_score.append([score,num_events])

    return(indiv_score,player_in_path)
#===============================================================================================#
def copy_files_tools(match_data):
    """ Copy files from source ot game_data folder """

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
