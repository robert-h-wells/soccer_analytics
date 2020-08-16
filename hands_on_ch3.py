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

import classification as clas

vals = mn.main()
total_data = vals[0]
nam = vals[1]

col_nam = ['Length','Num',*nam,'Score']
data_json = pd.DataFrame(total_data,columns=col_nam)


from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(data_json, test_size=0.2, random_state=42)
data = train_set.copy()

data = data_json.drop('Score',axis=1)
data_labels = data_json['Score'].copy()

from sklearn.svm import SVC
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
svm_clf = SVC()
svm_clf.fit(data, data_labels)
print('First trial',svm_clf.fit(data, data_labels))
some_digit = data.iloc[10]
print(svm_clf.predict([some_digit])) ; print()
some_digit_scores = svm_clf.decision_function([some_digit])
print(some_digit_scores)


print('3rd')
model3_type = clas.classification(data, data_labels, 'svc')
model3_type.init_fit()
check = model3_type.predictor([some_digit])
check2 = model3_type.predict_scores([some_digit])
print(check) 
print(check2) ; print()




# This looks strange
#y_train_pred = cross_val_predict(svm_clf,data, data_labels, cv=3)
#conf_mx = confusion_matrix(data_labels, y_train_pred)
#print(conf_mx)

if 1==0:
    from sklearn.linear_model import LogisticRegression
    softmax_reg = LogisticRegression(multi_class="multinomial",solver="lbfgs", C=10)
    softmax_reg.fit(data, data_labels)
    print(softmax_reg.predict(some_digit))