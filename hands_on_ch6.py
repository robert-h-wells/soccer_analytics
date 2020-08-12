import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation
import json
from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from scipy.interpolate import griddata
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.preprocessing import PolynomialFeatures

import tools as tl
import plots as pl
import pass_paths as mn 


vals = mn.main()
total_data = vals[0]
nam = vals[1]

col_nam = ['Length','Num',*nam,'Score']
data_json = pd.DataFrame(total_data,columns=col_nam)
data = data_json.drop('Score',axis=1)
data_labels = data_json['Score'].copy()
data_labels_val = list(set(data_labels))

data_labels_new = data_labels
for i in range(len(data_labels)):
    if data_labels[i] > 0:
        data_labels_new[i] = 1
    else:
        data_labels_new[i] = 0

data_labels_val_new = list(set(data_labels_new))

print(str(data_labels_val))
blah = ['A','B','C','D','E','F','G','H','I','J']


from sklearn.tree import DecisionTreeClassifier

tree_clf = DecisionTreeClassifier(max_depth=3)
tree_clf.fit(data, data_labels)

from sklearn.tree import export_graphviz

f = open("pathway_scores.dot", 'w')
export_graphviz(
        tree_clf,
        out_file=f,
        feature_names=['Length','Num',*nam],
        class_names=['Bad','Good'],
        rounded=True,
        filled=True
    )
