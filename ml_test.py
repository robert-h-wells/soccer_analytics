import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation
from sklearn.pipeline import Pipeline
from scipy.interpolate import griddata

import full_season as mn
import tools as tl
import plots as pl


def ml_models(df,df_nam,nam,event_nam):

    checks = [2,6,7,9,10,11,12,13,23,24]
    check_nam = [df_nam[i] for i in checks]
    print(check_nam)

    for i in range(len(checks)):
        x2 = check_nam[i]

        print(x2,len(list(df['Score'] [(df['Score'] == 10) & (df[x2] == 1) ])),
            len(list(df['Score'] [(df['Score'] != 10) & (df[x2] == 1) ])) )

    #X = df[df_nam[:-1]]
    X = df[check_nam]
    target = df['Score']

    target_10 = ([df['Score'] == 10])
    # Need to improve this to shot being the highest variable

    from sklearn.ensemble import RandomForestClassifier

    forest_clf = RandomForestClassifier()
    forest_clf.fit(X, target_10[0])

    important_param = sorted(zip([round(j,4) for j in forest_clf.feature_importances_],
                        check_nam), reverse=True)
    
    for i in important_param:
      print(i)    
      
# NOW NEED TO WORK ON REGRESSION, CATEGORIES FOR EACH PATHWAY FROM BOOK EXAMPLES


#=============================================================================================================#