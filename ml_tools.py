#===============================================================================================#
import numpy as np
import matplotlib.pyplot as plt
#===============================================================================================#
def find_cluster(X,val):
    """
    Find clusters of data with K-Means. Finds the best number of clusters through 
    silhouette score.
    """

    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    chosen = 0 ; chosen_score = 0.0
    for j in range(val[0],val[1]):
        kmeans = KMeans(n_clusters=j, random_state=42).fit(X)
        if silhouette_score(X, kmeans.labels_) > chosen_score:
            chosen_score = silhouette_score(X, kmeans.labels_)
            chosen = j

    kmeans = KMeans(n_clusters=chosen, random_state=42).fit(X)

    return(kmeans)
#===============================================================================================#