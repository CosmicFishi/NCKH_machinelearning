from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def read_dataset():
    pass


def get_vector(data_train, data_test=None):
    # this is a book
    vector = TfidfVectorizer(stop_words=['này'])

    train_vectors = vector.fit_transform(data_train)
    test_vectors = None
    if data_test:
        test_vectors = vector.transform(data_test)

    print("CAC TRUC: " + str(vector.get_feature_names()))

    return train_vectors, test_vectors


def naive_bayes_train(train_vectors, train_target):
    classifier = MultinomialNB(alpha=0.01)
    classifier.fit(train_vectors, train_target)

    return classifier


def naive_bayes_predict(classifier, test_vectors):
    return classifier.predict(test_vectors)

if __name__ == '__main__':
    from old.dht.helper import Helper
    m = Helper.w2v_model()
    import pdb
    pdb.set_trace()
    corpus = ['sản_phẩm này rất tốt',
              'tôi rất thích máy này',
              'máy chậm',
              'màn_hình sáng, tuyệt_vời',
              'thiết_kế xấu',
              'chụp_hình xấu',
              'đẹp']
    target =  [1, 1, -1, 1, -1, -1, 1]
    corpus_test = ['sản_phẩm có thiết_kế xấu', 'máy đẹp']
    train_vectors, test_vectors = get_vector(corpus, corpus_test)
    #
    cls = naive_bayes_train(train_vectors, target)
    results = naive_bayes_predict(cls, test_vectors)
    print(results)

    # print("INFO (so tai lieu, so truc vector):" + str(train_vectors.shape))
    # print(train_vectors.todense())