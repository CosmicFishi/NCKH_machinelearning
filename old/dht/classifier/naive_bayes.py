from dht.classifier.base import BaseClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB


class MultinomialNBClassifier(BaseClassifier):
    def __init__(self, alpha=0.01):
        params = {
            "alpha": alpha
        }

        super().__init__(class_name=MultinomialNB.__name__,
                         params=params)


class BernoulliNBClassifier(BaseClassifier):
    def __init__(self, alpha=0.01):
        params = {
            "alpha": alpha
        }

        super().__init__(class_name=BernoulliNB.__name__,
                         params=params)
