from sklearn.model_selection import KFold

from dht.classifier.ensemble import OvoClassifier, OvrClassifier
from dht.classifier.logistic_regression import LogisticRegressionClassifier
from dht.classifier.svm import SvmClassifier
from dht.dataset.by_category import CategoryDataset
from dht.feature_extraction.tfidf import TfIdfVec
from dht.helper import Helper


def split_validate(dataset_path):
    c = CategoryDataset(path=dataset_path, is_replace_not_terms=True, is_replace_emotion_icons=True)
    ds = c.load_dataset()

    result = Helper.split_dataset(ds.feature, ds.target, test_size=0.2)
    X_train, y_train = result["X_train"], result["y_train"]
    X_test, y_test = result["X_test"], result["y_test"]

    params = {
        "ngram_range": (1, 2)
    }

    vector = TfIdfVec(ds_train=X_train, ds_test=X_test, params=params).vectorizer()
    train_vectors = vector["train_vectors"]
    test_vectors = vector["test_vectors"]
    #
    # from dht.deep.test import train
    # train(train_vectors, y_train, test_vectors, y_test)

    print("=== LOGISTIC REGRESSION MULTINOMIAL ===")
    clf = LogisticRegressionClassifier(multi_class="multinomial")
    clf.training(train_vectors=train_vectors, train_targets=y_train)
    re1 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    print(re1)
    print("=== SVM RBF ===")
    clf = SvmClassifier(kernel="rbf")
    re2 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    print(re2)
    print("=== OVO ===")
    clf = OvoClassifier()
    clf.training(train_vectors=train_vectors, train_targets=y_train)
    re3 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    print(re3)
    print("=== OVR ===")
    clf = OvrClassifier()
    clf.training(train_vectors=train_vectors, train_targets=y_train)
    re4 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    print(re4)


def cross_validate(k=5,
                   dataset_path="/Users/duonghuuthanh/Desktop/My-projects/SentimentAnalysis/2018/dataset4/data_train/train"):
    c = CategoryDataset(path=dataset_path,
                        is_remove_special_character=True, is_replace_not_terms=True,
                        is_remove_number=True, is_indicate_phrases=True, is_replace_emotion_icons=True)
    dataset = c.load_dataset()

    X = dataset.feature
    y = dataset.target

    kf = KFold(n_splits=k, shuffle=True)
    split_dataset = [(train_index, test_index) for train_index, test_index in kf.split(X)]

    score0, score1, score2, score3, score4, score5, score6, score7, score8, score9 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    pre0, pre1, pre2, pre3, pre4, pre5, pre6, pre7, pre8, pre9 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    tr0, tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8, tr9 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for train_index, test_index in split_dataset:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        params = {
            "ngram_range": (1, 2)
        }
        result = TfIdfVec(ds_train=X_train, ds_test=X_test, params=params).vectorizer()
        # result = ChiSquareVec(ds_train=X_train, ds_test=X_test, params=params, y_train=y_train).vectorizer()

        train_vectors = result["train_vectors"]
        test_vectors = result["test_vectors"]

        # print("=== KNN LINEAR ===")
        # clf = LogisticRegressionClassifier()
        # tr0 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re0 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re0)
        print("=== LOGISTIC REGRESSION MULTINOMIAL ===")
        clf = LogisticRegressionClassifier(multi_class="multinomial")
        tr1 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        re1 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        print(re1)
        # print("=== SVM RBF ===")
        # clf = SvmClassifier(kernel="rbf")
        # tr2 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re2 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re2)
        # print("=== SVM LINEAR ===")
        # clf = SvmClassifier(kernel="linear")
        # tr3 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re3 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re3)
        # print("=== RANDOM FOREST 10 subtrees ===")
        # clf = RandForestClassifier()
        # tr4 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re4 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re4)
        # print("=== RANDOM FOREST 50 subtrees ===")
        # clf = RandForestClassifier(subtrees=50)
        # tr5 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re5 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re5)
        # print("=== RANDOM FOREST 80 subtrees ===")
        # clf = RandForestClassifier(subtrees=80)
        # tr6 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re6 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re6)
        # print("=== RANDOM FOREST 100 subtrees ===")
        # clf = RandForestClassifier(subtrees=100)
        # tr7 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re7 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re7)
        # print("=== OVO ===")
        # clf = OvoClassifier()
        # tr8 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re8 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re8)
        # print("=== OVR ===")
        # clf = OvrClassifier()
        # tr9 += clf.training(train_vectors=train_vectors, train_targets=y_train)["duration"]
        # re9 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
        # print(re9)

        # score0 += re0["f1_score"]
        score1 += re1["f1_score"]
        # score2 += re2["f1_score"]
        # score3 += re3["f1_score"]
        # score4 += re4["f1_score"]
        # score5 += re5["f1_score"]
        # score6 += re6["f1_score"]
        # score7 += re7["f1_score"]
        # score8 += re8["f1_score"]
        # score9 += re9["f1_score"]

        # pre0 += re0["duration"]
        pre1 += re1["duration"]
        # pre2 += re2["duration"]
        # pre3 += re3["duration"]
        # pre4 += re4["duration"]
        # pre5 += re5["duration"]
        # pre6 += re6["duration"]
        # pre7 += re7["duration"]
        # pre8 += re8["duration"]
        # pre9 += re9["duration"]

    print("Logistic regression linear: ", score0/5, pre0/5, tr0/5)
    print("Logistic regression multinomimal: ", score1/5, pre1/5, tr1/5)
    print("SVM RBF: ", score2/5, pre2/5, tr2/5)
    print("SVM LINEAR: ", score3/5, pre3/5, tr3/5)
    print("RANDOM FOREST 10: ", score4/5, pre4/5, tr4/5)
    print("RANDOM FOREST 50: ", score5/5, pre5/5, tr5/5)
    print("RANDOM FOREST 80: ", score6/5, pre6/5, tr6/5)
    print("RANDOM FOREST 100: ", score7/5, pre7/5, tr7/5)
    print("OVO: ", score8/5, pre8/5, tr8/5)
    print("OVR: ", score9/5, pre9/5, tr9/5)


if __name__ == "__main__":
    pass
