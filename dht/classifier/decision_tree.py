from dht.classifier.base import BaseClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


class DecTreeClassifier(BaseClassifier):
    def __init__(self, max_depth=None):
        params = {
            "max_depth": max_depth
        }

        super().__init__(class_name=DecisionTreeClassifier.__name__,
                         params=params)


class RandForestClassifier(BaseClassifier):
    def __init__(self, subtrees=10):
        params = {
            "n_estimators": subtrees
        }

        super().__init__(class_name=RandomForestClassifier.__name__,
                         params=params)
