from dht.classifier.base import BaseClassifier
from sklearn.neighbors import KNeighborsClassifier


class KNNClassifier(BaseClassifier):
    def __init__(self, k=1):
        params = {
            "n_neighbors": k,
            "p": 2
        }

        super().__init__(class_name=KNeighborsClassifier.__name__,
                         params=params)
