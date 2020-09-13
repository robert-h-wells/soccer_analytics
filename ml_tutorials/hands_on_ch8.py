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


from sklearn.decomposition import PCA

pca = PCA(n_components = 2)
X2D = pca.fit_transform(data)
print(pca.explained_variance_ratio_)

pca = PCA()
pca.fit(data)
cumsum = np.cumsum(pca.explained_variance_ratio_)
d = np.argmax(cumsum >= 0.95) + 1
print(d)

if 1==0:
    plt.figure(figsize=(6,4))
    plt.plot(cumsum, linewidth=3)
    plt.axis([0, 400, 0, 1])
    plt.xlabel("Dimensions")
    plt.ylabel("Explained Variance")
    plt.show()


# Kernel PCA
from sklearn.decomposition import KernelPCA

rbf_pca = KernelPCA(n_components = 2, kernel="rbf", gamma=0.04)
X_reduced = rbf_pca.fit_transform(data)


from sklearn.model_selection import GridSearchCV

clf = Pipeline([
        ("kpca", KernelPCA(n_components=2)),
        ("log_reg", LogisticRegression())
    ])

param_grid = [{
        "kpca__gamma": np.linspace(0.03, 0.05, 10),
        "kpca__kernel": ["rbf", "sigmoid"]
    }]

grid_search = GridSearchCV(clf, param_grid, cv=3)
grid_search.fit(data, data_labels)
print(grid_search.best_params_)