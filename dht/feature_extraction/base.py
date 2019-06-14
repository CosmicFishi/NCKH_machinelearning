from sklearn.feature_extraction.text import TfidfVectorizer


class BaseVectorizer:
    def __init__(self, ds_train, ds_test, class_name=None, params=None):
        self.class_name = class_name
        self.params = params
        self.ds_train = ds_train
        self.ds_test = ds_test

    def vectorizer(self):
        train_vectors, test_vectors = self._process()

        return {
            "train_vectors": train_vectors,
            "test_vectors": test_vectors
        }

    def _process(self):
        v = globals()[self.class_name](**self.params)
        train_vectors = v.fit_transform(self.ds_train)
        test_vectors = v.transform(self.ds_test)

        return train_vectors, test_vectors

