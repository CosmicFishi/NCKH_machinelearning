from dht.feature_extraction.base import BaseVectorizer
from sklearn.feature_extraction.text import HashingVectorizer


class HashVectorizer(BaseVectorizer):
    def __init__(self, params, ds_train, ds_test):
        super().__init__(ds_train=ds_train,
                         ds_test=ds_test,
                         class_name=HashingVectorizer.__name__,
                         params=params)

    def process(self):
        v = globals()[self.class_name](**self.params)
        train_vectors = v.transform(self.ds_train)
        test_vectors = v.transform(self.ds_test)

        return train_vectors, test_vectors
