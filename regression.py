#==================================================================================#
class regression:
    """

    """

    def __init__(self,X=0,labels=0,name='linear',rand=42):
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

    def init_fit(self,c_val=1,degree_val=2):
        if self.name == 'linear':
            from sklearn.linear_model import LinearRegression
            self.model = lin_reg = LinearRegression()

        elif self.name == 'sgd':
            from sklearn.linear_model import SGDRegressor
            self.model = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1)

        elif self.name == 'svm':
            from sklearn.svm import LinearSVR
            self.model = LinearSVR(epsilon=1.5)

        elif self.name == 'svm_poly':
            from sklearn.svm import SVR
            svm_poly_reg = SVR(kernel="poly", degree=degree_val, C=c_val, epsilon=0.1)

        elif self.name == 'poly':
            # NEED TO FIND THE CODE FOR THIS, just using SVM with PolynomialFeatures atm
            self.model = LinearRegression()

        elif self.name == 'ridge':
            from sklearn.linear_model import Ridge
            self.model = Ridge(alpha=1, solver="cholesky")

        elif self.name == 'sgd_ridge':
            from sklearn.linear_model import SGDRegressor
            self.model = SGDRegressor(penalty="l2")

        elif self.name == 'lasso':
            from sklearn.linear_model import Lasso
            self.name = Lasso(alpha=0.1)

        elif self.name == 'elastic':
            from sklearn.linear_model import ElasticNet
            self.model = ElasticNet(alpha=0.1, l1_ratio=0.5)
            
        elif self.name == 'logistic':
            from sklearn.linear_model import LogisticRegression
            self.model = LogisticRegression()

        elif self.name == 'softmax':
            from sklearn.linear_model import LogisticRegression
            self.model = LogisticRegression(multi_class="multinomial",solver="lbfgs", C=c_val)

        else:
            print('No correct model given.')
            print('Try again with sgd, rand_forest, svc, kneighbors')
            return()

        return(self.model)


    def predictor(self,predict_val):
        return_val = self.model.predict(predict_val)
        return(return_val)

    # need to make function for intercept and coef after fit
    def coefficients(self):
        return(self.model.intercept_, self.model.coef_)

#==================================================================================#

if 1==0:
    # Linear Regression
    lin_reg.intercept_, lin_reg.coef_

    # Stochastic Gradient Descent
    sgd_reg.intercept_, sgd_reg.coef_

    # Polynomial Regression
    lin_reg.fit(X_poly, y)
    # Need to look into this, might have to change self.X to this X_poly
