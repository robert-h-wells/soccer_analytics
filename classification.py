# want to make classes for each type of classification model
# SVM

# Possibly might make one large class and have the specific classifiers in it

#==================================================================================#
class classification:
    """
    Contains SGD and SVC classification classifiers.
    Return prediction value and prediction scores.
    """

    def __init__(self,X=0,labels=0,name='sgd',rand=42):
        self.X = X
        self.labels = labels
        self.name = name
        self.model = []
        self.values = 0
        self.return_val = 0
        self.scores = 0
        self.rand = rand

    def init_fit(self):
        if self.name == 'sgd':
            from sklearn.linear_model import SGDClassifier
            self.model = SGDClassifier(random_state=self.rand)
        elif self.name == 'svc':
            from sklearn.svm import SVC
            self.model = SVC()

        self.model.fit(self.X, self.labels)
        return(self.model)

    def predictor(self,predict_val):
        self.return_val = self.model.predict(predict_val)
        return(self.return_val)

    def predict_scores(self,predict_val):
        self.scores = self.model.decision_function(predict_val)
        return(self.scores)

    def cross_valid():  # Needs work
        from sklearn.model_selection import cross_val_score
        cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy")

    def confus_mat():  # Needs work
        from sklearn.model_selection import cross_val_predict
        from sklearn.metrics import confusion_matrix
        y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3)
        confusion_matrix(y_train_5, y_train_pred)

#==================================================================================#