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

import tools as tl
import plots as pl
import pass_paths as mn 

def plot_decision_boundary(clf, X, y, axes=[0, 7.5, 0, 3], iris=True, legend=False, plot_training=True):
    x1s = np.linspace(axes[0], axes[1], 100)
    x2s = np.linspace(axes[2], axes[3], 100)
    x1, x2 = np.meshgrid(x1s, x2s)
    X_new = np.c_[x1.ravel(), x2.ravel()]
    y_pred = clf.predict(X_new).reshape(x1.shape)
    custom_cmap = ListedColormap(['#fafab0','#9898ff','#a0faa0'])
    plt.contourf(x1, x2, y_pred, alpha=0.3, cmap=custom_cmap)
    if not iris:
        custom_cmap2 = ListedColormap(['#7d7d58','#4c4c7f','#507d50'])
        plt.contour(x1, x2, y_pred, cmap=custom_cmap2, alpha=0.8)
    if plot_training:
        plt.plot(X[:, 0][y==0], X[:, 1][y==0], "yo", label="Iris setosa")
        plt.plot(X[:, 0][y==1], X[:, 1][y==1], "bs", label="Iris versicolor")
        plt.plot(X[:, 0][y==2], X[:, 1][y==2], "g^", label="Iris virginica")
        plt.axis(axes)
    if iris:
        plt.xlabel("Petal length", fontsize=14)
        plt.ylabel("Petal width", fontsize=14)
    else:
        plt.xlabel(r"$x_1$", fontsize=18)
        plt.ylabel(r"$x_2$", fontsize=18, rotation=0)
    if legend:
        plt.legend(loc="lower right", fontsize=14)

def plot_regression_predictions(tree_reg, X, y, axes=[0, 1, -0.2, 1], ylabel="$y$"):
    x1 = np.linspace(axes[0], axes[1], 500).reshape(-1, 1)
    y_pred = tree_reg.predict(x1)
    plt.axis(axes)
    plt.xlabel("$x_1$", fontsize=18)
    if ylabel:
        plt.ylabel(ylabel, fontsize=18, rotation=0)
    plt.plot(X, y, "b.")
    plt.plot(x1, y_pred, "r.-", linewidth=2, label=r"$\hat{y}$")




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

data_labels = data_json['Score'].copy()
data_labels_val = list(set(data_labels))

data_labels_new = data_labels
if 1==0:
    for i in range(len(data_labels)):
        if data_labels[i] > 0:
            data_labels_new[i] = 1
        else:
            data_labels_new[i] = 0

if 1==1:
    for i in range(len(data_labels)):
        if X[i,1] > 5 and X[i,0] > 15:
            data_labels_new[i] = 1
        else:
            data_labels_new[i] = 0

data_labels_val_new = list(set(data_labels_new))

print(str(data_labels_val))
blah = ['A','B','C','D','E','F','G','H','I','J']


from sklearn.tree import DecisionTreeClassifier

tree_clf = DecisionTreeClassifier(max_depth=5)
tree_clf.fit(X, data_labels)

from sklearn.tree import export_graphviz

f = open("pathway_scores.dot", 'w')
export_graphviz(
        tree_clf,
        out_file=f,
        feature_names=['Length','Num'],
        class_names=['Bad','Good'],
        rounded=True,
        filled=True
    )


plot_decision_boundary(tree_clf, X, data_labels, axes=[min(X[:,0]),max(X[:,0]),min(X[:,1]),max(X[:,1])])
plt.show()

print(tree_clf.predict_proba([[10,2]]))

# Regression
if 1==1:   # not working with my data
    tree_reg = DecisionTreeRegressor(random_state=42, max_depth=2)
    # need to change X to a 1d array
    X2 = X[:,0]
    tree_reg.fit(X2, data_labels)
    plot_regression_predictions(tree_reg, X2, data_labels, axes=[min(X[:,0]),max(X[:,0]),min(X[:,1]),max(X[:,1])])
    plt.show()

np.random.seed(42)
m = 200
X = np.random.rand(m, 1)
y = 4 * (X - 0.5) ** 2
y = y + np.random.randn(m, 1) / 10
from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor(max_depth=2, random_state=42)
tree_reg.fit(X, y)
tree_reg1 = DecisionTreeRegressor(random_state=42, max_depth=2)
tree_reg2 = DecisionTreeRegressor(random_state=42, max_depth=3)
tree_reg1.fit(X, y)
tree_reg2.fit(X, y)

fig, axes = plt.subplots(ncols=2, figsize=(10, 4), sharey=True)
plt.sca(axes[0])
plot_regression_predictions(tree_reg1, X, y)
for split, style in ((0.1973, "k-"), (0.0917, "k--"), (0.7718, "k--")):
    plt.plot([split, split], [-0.2, 1], style, linewidth=2)
plt.text(0.21, 0.65, "Depth=0", fontsize=15)
plt.text(0.01, 0.2, "Depth=1", fontsize=13)
plt.text(0.65, 0.8, "Depth=1", fontsize=13)
plt.legend(loc="upper center", fontsize=18)
plt.title("max_depth=2", fontsize=14)

plt.sca(axes[1])
plot_regression_predictions(tree_reg2, X, y, ylabel=None)
for split, style in ((0.1973, "k-"), (0.0917, "k--"), (0.7718, "k--")):
    plt.plot([split, split], [-0.2, 1], style, linewidth=2)
for split in (0.0458, 0.1298, 0.2873, 0.9040):
    plt.plot([split, split], [-0.2, 1], "k:", linewidth=1)
plt.text(0.3, 0.5, "Depth=2", fontsize=13)
plt.title("max_depth=3", fontsize=14)

plt.show()