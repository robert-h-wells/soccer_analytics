# Class for all classification algorithms used.

# Functions for individual predictions, scores of invidividual precitions,
# cross validiation scores, confusion matrix, and precision and recall scores.

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
        self.rand = rand

    def init(self,val=0,degree_val=2):  # Pre-processing data
        if val == 1:
            from sklearn.preprocessing import StandardScaler
            return(StandardScaler())
        elif val == 2:
            from sklearn.preprocessing import PolynomialFeatures
            return(PolynomialFeatures(degree=degree_val, include_bias=False))

    def init_fit(self,c_val=1):
        if self.name == 'sgd':
            from sklearn.linear_model import SGDClassifier
            self.model = SGDClassifier(random_state=self.rand)

        elif self.name =='rand_forest':
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(random_state=self.rand)

        elif self.name == 'svm':
            from sklearn.svm import SVC
            self.model = SVC()

        elif self.name == 'poly_kernel':
            from sklearn.svm import SVC
            self.model = SVC(kernel="poly", degree=3, coef0=1, C=5)

        elif self.name == 'gauss_rbf_kernel':
            from sklearn.svm import SVC
            self.model = SVC(kernel="rbf", gamma=5, C=10)

        elif self.name == 'linear_svm':
             from sklearn.svm import LinearSVC
             self.model = LinearSVC(C=c_val, loss="hinge")

        elif self.name == 'kneighbors':
            from sklearn.neighbors import KNeighborsClassifier
            self.model = KNeighborsClassifier()

        else:
            print('No correct model given.')
            print('Try again with sgd, rand_forest, svc, kneighbors')
            return()

        return(self.model)


    def predictor(self,predict_val):
        return_val = self.model.predict(predict_val)
        return(return_val)

    def predict_scores(self,predict_val):
        scores = self.model.decision_function(predict_val)
        return(scores)

    def cross_valid(self,num=5):
        from sklearn.model_selection import cross_val_score
        cross_scores = cross_val_score(self.model, self.X, self.labels, cv=num, scoring="accuracy")
        return(cross_scores)

    def confus_mat(self,num=5):
        from sklearn.model_selection import cross_val_predict
        from sklearn.metrics import confusion_matrix
        y_pred = cross_val_predict(self.model, self.X, self.labels, cv=num)
        mat_scores = confusion_matrix(self.labels, y_pred)
        return(mat_scores)

    def prec_recall():
        from sklearn.model_selection import cross_val_predict
        from sklearn.metrics import precision_score, recall_score
        y_pred = cross_val_predict(self.model, self.X, self.labels, cv=num)
        prec = precision_score(self.labels, y_pred)
        recall = recall_score(y_train_5, y_train_pred)
        return(prec,recall)

#==================================================================================#