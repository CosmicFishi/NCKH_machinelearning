import os

ROOT = os.path.abspath("..")


class FastTextClassifier:
    def __init__(self):
        pass

    def train(self):
        os.system("{0}/fastText/fasttext supervised -input {0}/dataset/fasttextdata.txt -output {0}/dataset/fasttextdata_model -label  __label__".format(ROOT))

    def predict(self):
        os.system("{0}/fastText/fasttext test {0}/dataset/fasttextdata_model.bin {0}/dataset/fasttextdata_test.txt".format(ROOT))

    def get_vector_of_sentence(self, sentence):
        re = os.popen("echo '{1}' | {0}/dataset/fastText/fasttext print-sentence-vectors {0}/dataset/fasttextdata_model.bin".format(ROOT, sentence))
        return [float(t) for t in re.read().replace(" \n", "").split()]


if __name__ == "__main__":
    FastTextClassifier().train()
    FastTextClassifier().predict()
