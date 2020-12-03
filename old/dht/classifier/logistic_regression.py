from dht.classifier.base import BaseClassifier
from sklearn.linear_model import LogisticRegression


class LogisticRegressionClassifier(BaseClassifier):
    def __init__(self, multi_class="ovr"):
        params = {
            "multi_class": multi_class,
            "solver": "lbfgs"
        }

        super().__init__(class_name=LogisticRegression.__name__,
                         params=params)