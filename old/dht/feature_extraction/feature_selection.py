from dht.feature_extraction.base import BaseVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2


class ChiSquareVec(BaseVectorizer):
    def __init__(self, params, ds_train, ds_test, y_train):
        super().__init__(params=params,
                         ds_train=ds_train,
                         ds_test=ds_test,
                         class_name=TfidfVectorizer.__name__)
        self.y_train = y_train

    def vectorizer(self):
        train_vectors, test_vectors = self.process()

        best = SelectKBest(score_func=chi2, k=10)
        f = best.fit(train_vectors, self.y_train)

        train_vectors = f.transform(train_vectors).toarray()
        test_vectors = f.transform(test_vectors).toarray()

        return {
            "train_vectors": train_vectors,
            "test_vectors": test_vectors
        }
