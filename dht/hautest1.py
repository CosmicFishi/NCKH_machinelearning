import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

ROOT = os.path.abspath("..")

def read_text_file(file_path, encoding="utf-8", is_readlines=False):
    """
    Read the data in the text file

    :param file_path: the path of the file
    :param encoding: encoding for reading file
    :param is_readlines: return the whole text or list of lines of text file
    :return: text or list read from file
    """
    with open("%s/%s" % (ROOT, file_path), "r+", encoding=encoding) as f:
        if is_readlines:
            text = [t.replace("\n", "") for t in f.readlines()]
        else:
            text = f.read().replace("\n", "")

    return text

def get_vector(data, test_data= None):

    vector = TfidfVectorizer(stop_words=['này'])

    train_vectors = vector.fit_transform(data)
    test_vector = None

    if(test_data):
        test_vector = vector.transform(test_data)

    # lấy tên từng cột trong vector
    print("CAC TRUC: " + str(vector.get_feature_names()))

    return train_vectors,test_vector

def huan_luyen_native_bayes(train_vector, test_vector):
    classifier = MultinomialNB(alpha=0.01)
    classifier.fit(train_vector, test_vector)

    return classifier


def du_doan(classifier, test_vector):
    return classifier.predict(test_vector)

if __name__ == "__main__":
    from dht.helper import Helper
    m = Helper.w2v_model()
    import pdb
    pdb.set_trace()