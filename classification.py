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

    def init_fit(self,c_val=1,depth=2):
        if self.name == 'sgd':
            from sklearn.linear_model import SGDClassifier
            self.model = SGDClassifier(random_state=self.rand)

        elif self.name == 'decis_tree':
            from sklearn.tree import DecisionTreeClassifier
            print('Depth == ',depth)
            self.model = DecisionTreeClassifier(max_depth=depth)

        elif self.name =='rand_forest':
            from sklearn.ensemble import RandomForestClassifier
            print('Lots of parameters already set!')
            self.model = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)

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

    def predict_percent(self,predict_val):
        pred_percent = self.model.predict_proba(predict_val)

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

    def prec_recall(self,num=5):
        from sklearn.model_selection import cross_val_predict
        from sklearn.metrics import precision_score, recall_score
        y_pred = cross_val_predict(self.model, self.X, self.labels, cv=num)
        prec = precision_score(self.labels, y_pred)
        recall = recall_score(self.labels, y_pred)
        return(prec,recall)

    def accuracy(self,test,x_test,y_test):
        from sklearn.metrics import accuracy_score
        self.model.fit(self.X, self.labels)
        y_pred = self.model.predict(x_test)
        val = accuracy_score(y_test, y_pred)
        return accuracy_score(y_test, y_pred)

#==================================================================================#
def plot_svc_decision_boundary(svm_clf, xmin, xmax):
    "Decision boundary of SVC model"

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
#==================================================================================#
def plot_predictions(clf, axes):
    "Dont remember what this one is for"

    x0s = np.linspace(axes[0], axes[1], 100)
    x1s = np.linspace(axes[2], axes[3], 100)
    x0, x1 = np.meshgrid(x0s, x1s)
    X = np.c_[x0.ravel(), x1.ravel()]
    y_pred = clf.predict(X).reshape(x0.shape)
    y_decision = clf.decision_function(X).reshape(x0.shape)
    plt.contourf(x0, x1, y_pred, cmap=plt.cm.brg, alpha=0.2)
    plt.contourf(x0, x1, y_decision, cmap=plt.cm.brg, alpha=0.1)
#==================================================================================#