import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from itertools import chain
from scipy.interpolate import griddata
from collections import Counter

from shutil import copyfile

import tools as tl
import plots as pl
import pass_paths as mn 

vals = mn.main()
total_data = vals[0]
nam = vals[1]

if 1==1:
    col_nam = ['Length','Num',*nam,'Score']
    data_json = pd.DataFrame(total_data,columns=col_nam)

    # Some plots of the data
    #data_json.hist(bins=10)
    #data_json.plot(kind='scatter',x="Length",y="Num")
    #plt.show()

    #print(data_json.describe()) ; print()
    #print(data_json.info()) ; print()
    
    #corr_matrix = data_json.corr()
    #print(corr_matrix["Score"])

    from sklearn.model_selection import train_test_split
    train_set, test_set = train_test_split(data_json, test_size=0.2, random_state=42)
    data = train_set.copy()

    data = data_json.drop('Score',axis=1)
    data_labels = data_json['Score'].copy()

    num_pipeline = Pipeline([
            ('std_scaler', StandardScaler()),
    ])

    data_prepared = num_pipeline.fit_transform(data)

    lin_reg = LinearRegression()
    lin_reg.fit(data, data_labels)
    print('Intercept and Coef')
    print(lin_reg.intercept_, lin_reg.coef_)

    some_data = data.iloc[:5]
    some_labels = data_labels.iloc[:5]
    some_data_prepared = num_pipeline.fit_transform(some_data)

    from sklearn.tree import DecisionTreeRegressor
    tree_reg = DecisionTreeRegressor()
    tree_reg.fit(data, data_labels)

    from sklearn.ensemble import RandomForestRegressor
    forest_reg = RandomForestRegressor()
    forest_reg.fit(data, data_labels)

    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(tree_reg, data, data_labels,
                         scoring="neg_mean_squared_error", cv=10)
    tree_rmse_scores = np.sqrt(-scores)
    print('Decison Tree')
    print(scores)
    print(scores.std()) ; print()

    lin_scores = cross_val_score(lin_reg, data, data_labels,
                        scoring="neg_mean_squared_error", cv=10)
    print('Linear Regression')
    print(lin_scores)
    print(lin_scores.std()) ; print()

    forest_scores = cross_val_score(forest_reg, data, data_labels,
                      scoring="neg_mean_squared_error", cv=10)
    print('Forest')
    print(forest_scores)
    print(forest_scores.std())


    from sklearn.model_selection import GridSearchCV

    param_grid = [
        {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
        {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},
      ]

    forest_reg = RandomForestRegressor()

    grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
                              scoring='neg_mean_squared_error',
                              return_train_score=True)

    grid_search.fit(data, data_labels)
    print(grid_search.best_params_)
    cvres = grid_search.cv_results_
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        print(np.sqrt(-mean_score), params)

    feature_importances = grid_search.best_estimator_.feature_importances_
    print( sorted(zip(feature_importances,['Length','Num',*nam]), reverse=True) )

    if 1==0:
        # Randomly split up data to train/test
        from sklearn.model_selection import train_test_split
        train_set, test_set = train_test_split(data_json, test_size=0.2, random_state=42)

        # Stratified sampling of data for train/test
        from sklearn.model_selection import StratifiedShuffleSplit
        split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        for train_index, test_index in split.split(data_json, data_json["Num"]):
            strat_train_set = data_json.loc[train_index]
            strat_test_set = data_json.loc[test_index]