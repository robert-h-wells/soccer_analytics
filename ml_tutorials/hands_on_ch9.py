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

def plot_centroids(centroids, weights=None, circle_color='w', cross_color='k'):
    if weights is not None:
        centroids = centroids[weights > weights.max() / 10]
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='o', s=30, linewidths=8,
                color=circle_color, zorder=10, alpha=0.9)
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=50, linewidths=50,
                color=cross_color, zorder=11, alpha=1)

def plot_decision_boundaries(clusterer, X, resolution=1000, show_centroids=True,
                             show_xlabels=True, show_ylabels=True):
    mins = X.min(axis=0) - 0.1
    maxs = X.max(axis=0) + 0.1
    xx, yy = np.meshgrid(np.linspace(mins[0], maxs[0], resolution),
                         np.linspace(mins[1], maxs[1], resolution))
    Z = clusterer.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]),
                cmap="Pastel2")
    plt.contour(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]),
                linewidths=1, colors='k')
    #plot_data(X)
    plt.scatter(X[:,0],X[:,1],c=y_pred)
    if show_centroids:
        plot_centroids(clusterer.cluster_centers_)

    if show_xlabels:
        plt.xlabel("$x_1$", fontsize=14)
    else:
        plt.tick_params(labelbottom=False)
    if show_ylabels:
        plt.ylabel("$x_2$", fontsize=14, rotation=0)
    else:
        plt.tick_params(labelleft=False)

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


from sklearn.cluster import KMeans
k = 3
kmeans = KMeans(n_clusters=k)
y_pred = kmeans.fit_predict(X)
print(kmeans.cluster_centers_)

#plt.scatter(X[:,0],X[:,1],c=y_pred)
fig, ax = plt.subplots()
plot_decision_boundaries(kmeans, X,show_centroids=False)

kmeans_per_k = [KMeans(n_clusters=k, random_state=42).fit(X)
                for k in range(1, 10)]
from sklearn.metrics import silhouette_score
print(silhouette_score(X, kmeans.labels_))
silhouette_scores = [silhouette_score(X, model.labels_)
                     for model in kmeans_per_k[1:]]

fig, ax = plt.subplots()
plt.plot(range(2, 10), silhouette_scores, "bo-")


# DBSCAN
from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=0.05, min_samples=5)
dbscan.fit(X)

dbscan2 = DBSCAN(eps=0.2, min_samples=5)
dbscan2.fit(X)

dbscan3 = DBSCAN(eps=1., min_samples=5)
dbscan3.fit(X)

fig, ax = plt.subplots(3,1)
ax[0].scatter(X[:,0],X[:,1],c=dbscan.labels_)
ax[1].scatter(X[:,0],X[:,1],c=dbscan2.labels_)
ax[2].scatter(X[:,0],X[:,1],c=dbscan3.labels_)
#plt.show()


# Gaussian Mixture
from sklearn.mixture import GaussianMixture
from matplotlib.colors import LogNorm

def plot_gaussian_mixture(clusterer, X, resolution=1000, show_ylabels=True):
    mins = X.min(axis=0) - 0.1
    maxs = X.max(axis=0) + 0.1
    xx, yy = np.meshgrid(np.linspace(mins[0], maxs[0], resolution),
                         np.linspace(mins[1], maxs[1], resolution))
    Z = -clusterer.score_samples(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z,
                 norm=LogNorm(vmin=1.0, vmax=30.0),
                 levels=np.logspace(0, 2, 12))
    plt.contour(xx, yy, Z,
                norm=LogNorm(vmin=1.0, vmax=30.0),
                levels=np.logspace(0, 2, 12),
                linewidths=1, colors='k')

    Z = clusterer.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z,
                linewidths=2, colors='r', linestyles='dashed')
    
    plt.plot(X[:, 0], X[:, 1], 'k.', markersize=2)
    plot_centroids(clusterer.means_, clusterer.weights_)

    plt.xlabel("$x_1$", fontsize=14)
    if show_ylabels:
        plt.ylabel("$x_2$", fontsize=14, rotation=0)
    else:
        plt.tick_params(labelleft=False)


gm = GaussianMixture(n_components=3, n_init=10)
gm.fit(X)
fig, ax = plt.subplots()
plot_gaussian_mixture(gm, X)
plt.show()