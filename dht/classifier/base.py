from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.svm import SVC
from sklearn import metrics
import time


class BaseClassifier:
    def __init__(self, class_name, params={}):
        self.class_name = class_name
        self.params = params
        self.classifier = None

    def training(self, train_vectors, train_targets):
        start = time.time()
        self.classifier = globals()[self.class_name](**self.params)
        self.classifier.fit(train_vectors, train_targets)
        end = time.time()

        return {"duration": end - start}

    def predict(self, test_vectors, test_targets=None):
        if self.classifier:
            start = time.time()
            predict = self.classifier.predict(test_vectors)
            end = time.time()

            result = {
                "duration": end - start
            }

            if test_targets is not None:
                result["f1_score"] = metrics.f1_score(test_targets, predict, average="macro")

            return result
        else:
            raise Exception("Please training first!")
