# want to make classes for each type of classification model
# SVM

class svc_multi:
    """ Creating a class which will fit and predict SVM multi-classification
    """

    from sklearn.svm import SVC
    from sklearn.model_selection import cross_val_predict
    from sklearn.metrics import confusion_matrix

    def __init__(self,X,labels):
        self.X = 0
        self.labels = []

    def init_fit():
        svm_clf = SVC()
        svm_clf.fit(self.X, self.labels)

    def predict(predict_val):
        values = svm_clf.predict([predict_valt])
        return(values)

    def predict_scores(predict_val):
        scores = svm_clf.decision_function([predict_val])
        return(scores)
