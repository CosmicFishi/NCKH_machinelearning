import os


class FastTextClassifier:
    def __init__(self):
        pass

    def train(self):
        os.system("./fastText/fasttext supervised -input ./dataset/fasttextdata.txt -output ./dataset/fasttextdata_model -label  __label__")

    def predict(self):
        os.system("./fastText/fasttext test ./dataset/fasttextdata_model.bin ./dataset/fasttextdata_test.txt")

    def get_vector_of_sentence(self, sentence):
        re = os.popen("echo '%s' | /Users/duonghuuthanh/PycharmProjects/machinelearingapp/fastText/fasttext print-sentence-vectors /Users/duonghuuthanh/PycharmProjects/machinelearingapp/dataset/fasttextdata_model.bin" % sentence)
        return [float(t) for t in re.read().replace(" \n", "").split()]
