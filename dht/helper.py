from sklearn.model_selection import train_test_split
from pyvi import ViTokenizer
import pandas as pd
import os
import re

ROOT = os.path.abspath(".")
print(ROOT)


class Helper:
    @staticmethod
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

    @staticmethod
    def read_json_file(file_path):
        text = Helper.read_text_file("%s/%s" % (ROOT, file_path))

        return text

    @staticmethod
    def duplicate_terms_list(text=[]):
        for t in text:
            if t.find(" ") >= 0:
                text.append(t.replace(" ", "_"))

        return text

    @staticmethod
    def load_wordnet_by_csv(file_path="dataset/sentiment/VietSentiWordnet_Ver1.3.5.csv"):
        """
        Load wordnets from csv file from VietSentiWordNet

        References: https://github.com/sonvx/VietSentiWordNet
        :param file_path:
        :return:words and their synonym words
        {
            "words": "",
            "synonym_words": ""
        }
        """
        df = pd.read_csv("%s/%s" % (ROOT, file_path))

        words = []
        synonym_words = []
        for w, s in zip(df["SynsetTerms"].values, df["Gloss"].values):
            t = (" ".join(re.split("#[0-9]", w.replace("\n", "")))).split()
            words = words + t
            synonym_words = synonym_words + [s.split(";")[0].replace("\n", "").strip()]*len(t)

        return {
            "words": words,
            "synonym_words": synonym_words
        }

    @staticmethod
    def load_wordnet_texts(folder_path="dataset/vi-wordnet"):
        """
        Load wordnets from a folder which contains wordnet files

        References: https://github.com/zeloru/vietnamese-wordnet
        :param folder_path:
        :return: list of each wordnet files
        """
        words = []
        for file in os.listdir("%s/%s" % (ROOT, folder_path)):
            words.append(Helper.read_text_file("%s/%s" % (folder_path, file), is_readlines=True))

        return words

    @staticmethod
    def split_dataset(feature, target, test_size=0.2):
        """
        Split the dataset into train set and test set.

        :param feature: data points
        :param target: the labels of data points respectively
        :param test_size: the percent of test set (default is 20%)
        :return: dictionary of (train set, train target set, test set, test target set)
        """
        train, test, y_train, y_test = train_test_split(feature, target,
                                                        test_size=test_size,
                                                        random_state=42)

        return {
            "X_train": train,
            "y_train": y_train,
            "X_test": test,
            "y_test": y_test
        }

    @staticmethod
    def convert_to_fasttext_data(input_path, output_path):
        write = open(output_path, "w+", encoding="utf-8")
        for cat in os.listdir(input_path):
            for fi in os.listdir("%s/%s" % (input_path, cat)):
                try:
                    file_path = "%s/%s/%s" % (input_path, cat, fi)
                    f = open(file_path, "r+", encoding="utf-8")
                    text = f.read()
                    content = "__label__%s %s\n" % (cat, text)
                    write.write(content)
                    f.close()
                except Exception as ex:
                    print("ERROR %s: %s" % (fi, str(ex)))

        write.close()

    @staticmethod
    def check_intersection(s1=[], s2=[]):
        return len(set(s1) & set(s2)) > 0

    @staticmethod
    def tokenize(source_path, destination_path):
        dirs = os.listdir(source_path)
        for d in dirs:
            folder_path = "%s/%s" % (destination_path, d)
            if not os.path.exists(folder_path):
                os.makedirs("%s/%s" % (destination_path, d))

            file_path = "%s/%s" % (source_path, d)
            files = os.listdir(file_path)
            print("%s..." % file_path)
            for f in files:
                print("--- ", f)
                new_file = "%s/%s" % (folder_path, f)

                try:
                    if not os.path.exists(new_file):
                        inp = open("%s/%s" % (file_path, f), "r+", encoding="utf-8")
                        content = inp.read()
                        inp.close()

                        content = ViTokenizer.tokenize(content.strip())

                        out = open(new_file, "w+", encoding="utf-8")
                        out.write(content.lower())
                        out.close()
                except Exception as ex:
                    print(ex)
