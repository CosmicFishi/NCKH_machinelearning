from dht.classifier.base import BaseClassifier
from sklearn.svm import SVC
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier


class OvoClassifier(BaseClassifier):
    def __init__(self):
        params = {
            "estimator": SVC(kernel="linear")
        }

        super().__init__(class_name=OneVsOneClassifier.__name__,
                         params=params)


class OvrClassifier(BaseClassifier):
    def __init__(self):
        params = {
            "estimator": SVC(kernel="linear")
        }

        super().__init__(class_name=OneVsRestClassifier.__name__,
                         params=params)
