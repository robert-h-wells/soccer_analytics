#===============================================================================================#
import numpy as np
import matplotlib.pyplot as plt
import json
#===============================================================================================#
def get_path_score(data,poss_list):
    # determine result of the possession pathway and give score

    poss_score = len(poss_list)*[None]
    poss_score[0] = 0 ; poss_score[1] = 0

    for i in range(2,len(poss_list)):
        val = poss_list[i][1]-1

        try:

            if data[val+1]['possession_team']['name'] == 'Arsenal':  # possesion stays
                if data[val+1]['play_pattern']['id'] == 2:  # caused a corner kick
                    poss_score[i] = 3
                elif data[val+1]['play_pattern']['id'] == 3:  # caused a free kick
                    poss_score[i] = 2
                elif data[val+1]['play_pattern']['id'] == 4:  # caused a throw in
                    poss_score[i] = 1
                elif data[val+1]['play_pattern']['id'] == 7:  # caused a goal kick
                    poss_score[i] = 1
                else:
                    print('NEW TYPE')

            ## ~~ Still need to look at the end result of a pathway that results from a turnover
                
            elif data[val+1]['possession_team']['name'] != 'Arsenal':  # possesion changes
                if data[val+1]['play_pattern']['id'] == 2:  # caused a corner kick 
                    poss_score[i] = -3
                elif data[val+1]['play_pattern']['id'] == 3:  # caused a free kick
                    poss_score[i] = -2
                elif data[val+1]['play_pattern']['id'] == 4:  # caused a throw in
                    poss_score[i] = -1
                elif data[val+1]['play_pattern']['id'] == 7:  # caused a goal kick
                    poss_score[i] = -1

                elif data[val+1]['play_pattern']['id'] == 1:  # open play, gave ball away
                    poss_score[i] = -2

                elif data[val]['type']['id'] == 18:  # kickoff from halftime
                    poss_score[i] = 0

                elif data[val+1]['type']['id'] == 23:
                    poss_score[i] = 1

                elif data[val]['goalkeeper']['type']['id'] in [26, 27, 28, 29, 30, 31, 32, 33, 34]:
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
                    print('NEW NEW')
                    print('')

            else:
                print('WTF')

        except KeyError as e:
            print('========================================================')
            print(str(e))
            print('hmmmmmmm')
            print('========================================================')

    return(poss_score)
#===============================================================================================#