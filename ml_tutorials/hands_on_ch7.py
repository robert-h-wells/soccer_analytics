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
from matplotlib.colors import ListedColormap
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression

import tools as tl
import plots as pl
import pass_paths as mn 

vals = mn.main()
total_data = vals[0]
nam = vals[1]

col_nam = ['Length','Num',*nam,'Score']
data_json = pd.DataFrame(total_data,columns=col_nam)
data_num = data_json['Num']
data_length = data_json['Length']
X = np.zeros((np.size(data_num),2))
X[:,0] = data_length
X[:,1] = data_num

data = data_json.drop('Score',axis=1)
data_labels = data_json['Score'].copy()
data_labels_val = list(set(data_labels))

data_labels_new = data_labels
if 1==1:
    for i in range(len(data_labels)):
        if data_labels[i] > 0:
            data_labels_new[i] = 1
        else:
            data_labels_new[i] = 0

if 1==0:
    for i in range(len(data_labels)):
        if X[i,1] > 5 and X[i,0] > 15:
            data_labels_new[i] = 1
        else:
            data_labels_new[i] = 0

data_labels_val_new = list(set(data_labels_new))

log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier()
svm_clf = SVC()

voting_clf = VotingClassifier(
    estimators=[('lr', log_clf), ('rf', rnd_clf), ('svc', svm_clf)],
    voting='hard')
voting_clf.fit(X, data_labels)

from sklearn.metrics import accuracy_score
for clf in (log_clf, rnd_clf, svm_clf, voting_clf):
    clf.fit(X, data_labels)
    y_pred = clf.predict(X)
    print(clf.__class__.__name__, accuracy_score(data_labels, y_pred))


from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bag_clf = BaggingClassifier(
    DecisionTreeClassifier(), n_estimators=500,
    max_samples=100, bootstrap=True, n_jobs=-1)
bag_clf.fit(X, data_labels)
y_pred = bag_clf.predict(X)


from sklearn.ensemble import RandomForestClassifier
rnd_clf = RandomForestClassifier(n_estimators=500, n_jobs=-1)
rnd_clf.fit(data, data_labels)
print()
for i,j in sorted(zip(['Length','Num',*nam],rnd_clf.feature_importances_),reverse=True,key=lambda x: x[1]):
    print(i,j)