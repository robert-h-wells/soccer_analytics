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

def plot_svc_decision_boundary(svm_clf, xmin, xmax):
    w = svm_clf['linear_svc'].coef_[0]
    b = svm_clf['linear_svc'].intercept_[0]
    print('w',w)
    print('b',b)

    # At the decision boundary, w0*x0 + w1*x1 + b = 0
    # => x1 = -w0/w1 * x0 - b/w1
    print('min max',xmin,xmax)
    x0 = np.linspace(xmin, xmax, 200)
    decision_boundary = -w[0]/w[1] * x0 - b/w[1]

    margin = 1/w[1]
    gutter_up = decision_boundary + margin
    gutter_down = decision_boundary - margin

    #svs = svm_clf.support_vectors_
    #plt.scatter(svs[:, 0], svs[:, 1], s=180, facecolors='#FFAAAA')
    plt.plot(x0, decision_boundary, "k-", linewidth=2)
    plt.plot(x0, gutter_up, "k--", linewidth=2)
    plt.plot(x0, gutter_down, "k--", linewidth=2)


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

# Want to change to two data labels only
if 1==0:
    data_labels_new = data_labels
    for i in range(len(data_labels)):
        if data_labels[i] > 0: 
            data_labels_new[i] = 1
        else: 
            data_labels_new[i] = 0

# Stupid but just trying out to check code
if 1==1:
    data_labels_new = data_labels
    for i in range(len(data_labels)):
        if X[i,1] > 5 and X[i,0] > 15:
            data_labels_new[i] = 1
        else:
            data_labels_new[i] = 0


# linear SVM
if 1==0:
    svm_clf = Pipeline([
            ("scaler", StandardScaler()),
            ("linear_svc", LinearSVC(C=1, loss="hinge")),
        ])

    svm_clf.fit(X, data_labels_new)

    X_scaled = svm_clf["scaler"].fit_transform(X)

    fig, ax = plt.subplots()
    plot_svc_decision_boundary(svm_clf, min(X_scaled[:,0]), max(X_scaled[:,0]))
    plt.scatter(X_scaled[:,0],X_scaled[:,1],c=data_labels_new)
    plt.show()

# polynomial SVM
polynomial_svm_clf = Pipeline([
        ("poly_features", PolynomialFeatures(degree=3)),
        ("scaler", StandardScaler()),
        ("svm_clf", LinearSVC(C=10, loss="hinge"))
    ])

X_scaled = polynomial_svm_clf["scaler"].fit_transform(X)

polynomial_svm_clf.fit(X, data_labels_new)


# Polynomial Kernel
poly_kernel_svm_clf = Pipeline([
        ("scaler", StandardScaler()),
        ("svm_clf", SVC(kernel="poly", degree=5, coef0=1, C=5))
    ])
poly_kernel_svm_clf.fit(X, data_labels_new)

# Gaussian RBF Kernel
rbf_kernel_svm_clf = Pipeline([
        ("scaler", StandardScaler()),
        ("svm_clf", SVC(kernel="rbf", gamma=5, C=10))
    ])
rbf_kernel_svm_clf.fit(X, data_labels_new)


def plot_predictions(clf, axes):
    x0s = np.linspace(axes[0], axes[1], 100)
    x1s = np.linspace(axes[2], axes[3], 100)
    x0, x1 = np.meshgrid(x0s, x1s)
    X = np.c_[x0.ravel(), x1.ravel()]
    y_pred = clf.predict(X).reshape(x0.shape)
    y_decision = clf.decision_function(X).reshape(x0.shape)
    plt.contourf(x0, x1, y_pred, cmap=plt.cm.brg, alpha=0.2)
    plt.contourf(x0, x1, y_decision, cmap=plt.cm.brg, alpha=0.1)

fig, ax = plt.subplots()
plot_predictions(poly_kernel_svm_clf,[min(X[:,0])-1,max(X[:,0])+1,min(X[:,1])-1,max(X[:,1])+1])
plt.scatter(X[:,0],X[:,1],c=data_labels_new)
plt.title('Poly Kernel')

fig, ax = plt.subplots()
plot_predictions(rbf_kernel_svm_clf,[min(X[:,0])-1,max(X[:,0])+1,min(X[:,1])-1,max(X[:,1])+1])
plt.scatter(X[:,0],X[:,1],c=data_labels_new)
plt.title('Gaussian RBF')

plt.show()
