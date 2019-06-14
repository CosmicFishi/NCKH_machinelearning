from dht.classifier.base import BaseClassifier
from sklearn.ensemble import RandomForestClassifier


class RandForestClassifier(BaseClassifier):
    def __init__(self, subtrees=10):
        params = {
            "n_estimators": subtrees
        }

        super().__init__(class_name=RandomForestClassifier.__name__,
                         params=params)
