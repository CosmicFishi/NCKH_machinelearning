from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from dht.feature_extraction.base import BaseVectorizer


class TfIdfVec(BaseVectorizer):
    def __init__(self, params, ds_train, ds_test):
        super().__init__(ds_train=ds_train,
                         ds_test=ds_test,
                         class_name=TfidfVectorizer.__name__,
                         params=params)


class TfVec(BaseVectorizer):
    def __init__(self, params, ds_train, ds_test):
        super().__init__(ds_train=ds_train,
                         ds_test=ds_test,
                         class_name=CountVectorizer.__name__,
                         params=params)

