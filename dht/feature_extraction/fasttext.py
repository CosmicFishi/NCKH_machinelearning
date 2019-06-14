from dht.feature_extraction.base import BaseVectorizer
from dht.fasttext import FastTextClassifier
from scipy.sparse import csr_matrix
import numpy as np


class FastTextVec(BaseVectorizer):
    def __init__(self, ds_train, ds_test):
        super().__init__(ds_train=ds_train, ds_test=ds_test)

    def _process(self):
        f = FastTextClassifier()

        train_vectors = []
        for d in self.ds_train:
            train_vectors.append(f.get_vector_of_sentence(d))

        test_vectors = []
        for d in self.ds_test:
            test_vectors.append(f.get_vector_of_sentence(d))

        train = csr_matrix((len(train_vectors), len(train_vectors[0])), dtype=np.float64)

        idx = 0
        for d in train_vectors:
            try:
                train[idx] = d
                idx = idx + 1
            except:
                pass

        test = csr_matrix((len(test_vectors), len(test_vectors[0])), dtype=np.float64)

        idx = 0
        for d in test_vectors:
            try:
                test[idx] = d
                idx = idx + 1
            except:
                pass

        return train, test
