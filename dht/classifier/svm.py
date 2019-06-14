from dht.classifier.base import BaseClassifier
from sklearn.svm import SVC


class SvmClassifier(BaseClassifier):
    def __init__(self, kernel="rbf", gamma="auto", C=1e5, degree=3, coef0=0):
        params = {
            "kernel": kernel,
            "gamma": gamma,
            "degree": degree,
            "coef0": coef0,
            "C": C
        }

        super().__init__(class_name=SVC.__name__, params=params)