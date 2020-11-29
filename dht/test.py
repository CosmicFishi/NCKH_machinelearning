
from dht.dataset.by_category import CategoryDataset, AugmentedDataset, AugmentedValidationDataset
from dht.feature_extraction.feature_selection import ChiSquareVec
from dht.feature_extraction.tfidf import TfIdfVec
from dht.feature_extraction.hashing import HashVectorizer
from dht.classifier.logistic_regression import LogisticRegressionClassifier
from dht.classifier.svm import SvmClassifier
from dht.classifier.ensemble import OvoClassifier, OvrClassifier
from dht.classifier.naive_bayes import MultinomialNBClassifier
from dht.helper import Helper
# from dht.deep.test import cnn, train as deep_train
import copy

SENTIMENT_STOPWORDS = ("\ufeff", "+", "", ".", ",", "!", "%", "...", ")", "(", "thì", "là", "và", "bị", "với",
                       "thế_nào", "?", "", "một_số", "mot_so", "thi", "la", "va", "bi", "voi", "trong",
                       "the_nao", " j ", "gì", "pin", "điện_thoại", "máy", "sản_phẩm", "pin", "plus", "tôi",
                       "tôii", "pro", "apple", "nokia", "samsung", "huawei", "oppo", "xiaomi")


def augmented_validate(dataset_path):
    ds = AugmentedValidationDataset(path=dataset_path)
    ds_train, ds_test = ds.load_one_class_train()
    print("=== ONE TRAIN ===", ds_train[0]["feature"])

    # original classifiers
    train, test = ds.load_augmented_dataset(ds_train, ds_test)
    re1 = validate(train, test)

    # pre-processing and lexicons
    flag = True
    params = {
        "ngram_range": (1, 2)
    }
    ds_train_bk, ds_test_bk = ds.pre_process_one_class_train(ds_train=copy.deepcopy(ds_train),
                                                             ds_test=copy.deepcopy(ds_test),
                                                             is_replace_not_terms=flag,
                                                             is_replace_emotion_icons=flag,
                                                             is_indicate_phrases=flag,
                                                             is_remove_special_character=flag)
    train, test = ds.load_augmented_dataset(ds_train=ds_train_bk,
                                            ds_test=ds_test_bk)
    re2 = validate(train, test, params=params)

    # augmentation
    is_augmented = True
    train, test = ds.load_augmented_dataset(ds_train=copy.deepcopy(ds_train),
                                            ds_test=copy.deepcopy(ds_test),
                                            is_augmented=is_augmented)
    re3 = validate(train, test, params=params)

    # pre-processing, lexicons and augmentation
    train, test = ds.load_augmented_dataset(ds_train=ds_train_bk,
                                            ds_test=ds_test_bk,
                                            is_augmented=is_augmented)
    re4 = validate(train, test, params=params)

    return [re1, re2, re3, re4]


def validate1(train_path, test_path, flag=False):
    train = CategoryDataset(path=train_path, is_replace_not_terms=flag, is_indicate_phrases=flag,
                            is_replace_emotion_icons=flag).load_dataset()
    test = CategoryDataset(path=test_path, is_replace_not_terms=flag, is_remove_number=flag,
                           is_remove_special_character=flag, is_indicate_phrases=flag,
                           is_replace_emotion_icons=flag).load_dataset()

    params = {
        "ngram_range": (1, 2)
    } #if flag else {}

    return validate(train, test, params=params)


def validate2(train_path, test_path, flag=True, **kwargs):
    train = AugmentedDataset(path=train_path,
                             is_replace_not_terms=flag,
                             is_indicate_phrases=flag,
                             is_replace_emotion_icons=flag,
                             is_remove_special_character=flag,
                             back_translation=kwargs.get("back_translation", False),
                             syntax_tree=kwargs.get("syntax_tree", False),
                             eda=kwargs.get("eda", False),
                             w2v=kwargs.get("w2v", False)).load_dataset()
    test = CategoryDataset(path=test_path, is_replace_not_terms=flag, is_remove_number=flag,
                           is_remove_special_character=flag, is_indicate_phrases=flag,
                           is_replace_emotion_icons=flag).load_dataset()

    params = {
         "ngram_range": (1, 2)
    } #if flag else {}

    return validate(train, test, params=params)


def validate(train, test, params={}):
    X_train, y_train = train.feature, train.target
    X_test, y_test = test.feature, test.target

    return classifier_execute(X_train, y_train, X_test, y_test, params=params)


def deep_execute(dataset_path):
    ds = AugmentedValidationDataset(path=dataset_path)
    ds_train, ds_test = ds.load_one_class_train()

    ds_train_bk, ds_test_bk = ds.pre_process_one_class_train(ds_train=copy.deepcopy(ds_train),
                                                             ds_test=copy.deepcopy(ds_test),
                                                             is_replace_not_terms=True,
                                                             is_replace_emotion_icons=True,
                                                             is_indicate_phrases=True,
                                                             is_remove_special_character=True)

    train, test = ds.load_augmented_dataset(ds_train_bk, ds_test_bk)

    X_train, y_train = train.feature, train.target
    X_test, y_test = test.feature, test.target

    params = {
        "ngram_range": (1, 2)
    }

    vector = TfIdfVec(ds_train=X_train, ds_test=X_test, params=params).vectorizer()

    # deep_train(vector["train_vectors"], y_train, vector["test_vectors"], y_test)


def classifier_execute(X_train, y_train, X_test, y_test, params):
    vector = TfIdfVec(ds_train=X_train, ds_test=X_test, params=params).vectorizer()
    # vector = ChiSquareVec(ds_train=X_train, ds_test=X_test, params=params, y_train=y_train).vectorizer()
    # vector = HashVectorizer(ds_train=X_train, ds_test=X_test, params=params).vectorizer()
    train_vectors = vector["train_vectors"]
    test_vectors = vector["test_vectors"]

    # print("=== MultinomialNBClassifier ===")
    # clf = MultinomialNBClassifier()
    # clf.training(train_vectors=train_vectors, train_targets=y_train)
    # re0 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    # print(re0)
    print("=== LOGISTIC REGRESSION MULTINOMIAL ===")
    clf = LogisticRegressionClassifier(multi_class="multinomial")
    clf.training(train_vectors=train_vectors, train_targets=y_train)
    re1 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    print("=== SVM RBF ===")
    clf = SvmClassifier(kernel="rbf")
    clf.training(train_vectors=train_vectors, train_targets=y_train)
    re2 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    print("=== OVO ===")
    clf = OvoClassifier()
    clf.training(train_vectors=train_vectors, train_targets=y_train)
    re3 = clf.predict(test_vectors=test_vectors, test_targets=y_test)
    print("=== OVR ===")
    clf = OvrClassifier()
    clf.training(train_vectors=train_vectors, train_targets=y_train)
    re4 = clf.predict(test_vectors=test_vectors, test_targets=y_test)

    return [re1['f1_score'], re2['f1_score'], re3['f1_score'], re4['f1_score']]


if __name__ == "__main__":
    epoches = 10
    rows = []
    headers = ["CLASSIFIERS", "MAX F-SCORE", "MIN F-SCORE"]
    classifiers = ["MultinomialNBClassifier", "Logistic Regression", "SVM RBF", "OVO", "OVR"]
    num_experiments = 4
    num_classifiers = 5

    # ONE-DOCUMENT RANDOMLY
    # for ds in range(1, 6):
    #     rows.append(["=====", "START DATASET %d" % ds, "====="])
    #     result_max = [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]
    #     result_min = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
    #     for _ in range(epoches):
    #         path = "/Users/duonghuuthanh/Desktop/My-projects/SentimentAnalysis/2018/augmentation/dataset%d/test" % ds
    #         # deep_execute(path)
    #         result = augmented_validate(dataset_path=path)
    #         for r in range(num_experiments):
    #             for c in range(num_classifiers):
    #                 if result[r][c] > result_max[r][c]:
    #                     result_max[r][c] = result[r][c]
    #                 if result[r][c] < result_min[r][c]:
    #                     result_min[r][c] = result[r][c]
    #
    #     print(result_max)
    #     print(result_min)
    #
    #     for ma, mi in zip(result_max, result_min):
    #         for idx in range(len(classifiers)):
    #             rows.append([classifiers[idx], ma[idx], mi[idx]])
    #         rows.append(headers)

    # FIXED VALIDATE
    rows = []
    for i in range(1, 6):
        print("=== DATASET %d ===" % i)
        train_path = "/home/kan_haungo/Desktop/machinelearningapp/dataset/dataset1/dataset1/train" % i
        test_path = "/home/kan_haungo/Desktop/machinelearningapp/dataset/dataset1/dataset1/test" % i
        # result1 = validate1(train_path=train_path, test_path=test_path)
        # result2 = validate1(train_path=train_path, test_path=test_path, flag=True)
        # result3 = validate2(train_path=train_path, test_path=test_path, flag=False, back_translation=True)
        # result4 = validate2(train_path=train_path, test_path=test_path, flag=False, w2v=True)
        # result5 = validate2(train_path=train_path, test_path=test_path, flag=False, syntax_tree=True)
        result6 = validate2(train_path=train_path, test_path=test_path, flag=False, eda=True)
        # result7 = validate2(train_path=train_path, test_path=test_path, flag=True, back_translation=True)
        # result8 = validate2(train_path=train_path, test_path=test_path, flag=True, w2v=True)
        # result9 = validate2(train_path=train_path, test_path=test_path, flag=True, syntax_tree=True)
        # result10 = validate2(train_path=train_path, test_path=test_path, flag=True, eda=True)
        classifiers = ["Logistic Regression", "SVM RBF", "OVO", "OVR"]
        for c, r6 in zip(classifiers, result6):
            rows.append([c, r6])
        rows.append(["classifiers", "Original", "Preprocessing",
                     "Back", "w2v", "Syntax", "eda", "pre Back", "pre w2v", "pre Syntax", "pre eda"])

    print("===KẾT QUẢ===")
    print(rows)

    from datetime import datetime
    Helper.write_csv_file("[4]aug-%d-%s-ensembles.csv" % (epoches, str(datetime.now())),
                          headers=headers, rows=rows)
