from sklearn.model_selection import train_test_split
from pyvi import ViTokenizer
from underthesea import sent_tokenize
from . import trans
from translate import Translator
from selenium import webdriver
from json.decoder import JSONDecodeError
from gensim.models import Word2Vec, Phrases
import pandas as pd
import os
import re
import csv
import spacy
import pickle
import time

ROOT = os.path.abspath("..")
AUGMENTATION_CACHE_PATH = "/Users/duonghuuthanh/iCloud Drive (Archive)/Desktop/My-projects/SentimentAnalysis/2020/"


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
    def read_text_file2(file_path, encoding="utf-8", is_readlines=False):
        """
        Read the data in the text file

        :param file_path: the path of the file
        :param encoding: encoding for reading file
        :param is_readlines: return the whole text or list of lines of text file
        :return: text or list read from file
        """
        with open(file_path, "r+", encoding=encoding) as f:
            if is_readlines:
                text = [t.replace("\n", "") for t in f.readlines()]
            else:
                text = f.read().replace("\n", "")

        return text

    @staticmethod
    def write_csv_file(file_name, headers=[], rows=[]):
        path = "%s/stats/%s" % (ROOT, file_name)
        with open(path, mode="w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)

    @staticmethod
    def write_text_file(path_file_name, content):
        with open(path_file_name, "w") as txt_file:
            txt_file.write(content)

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
    def w2v_model(folder_path="/Users/duonghuuthanh/PycharmProjects/machinelearingapp/dataset/reviews"):
        def read_file(path):
            sentences = []
            for file in os.listdir(path):
                try:
                    d = "%s/%s" % (path, file)
                    if os.path.isdir(d):
                        return sentences + read_file(d)
                    else:
                        text = Helper.read_text_file2("%s/%s" % (path, file))
                        sentences = sentences + [sentence.split(" ") for sentence in Helper.tokenize_sentence(text)]
                except:
                    pass

            return sentences

        if os.path.exists("/Users/duonghuuthanh/PycharmProjects/machinelearingapp/dataset/w2v_train_model.sav"):
            model = Helper.load_cache_file("/Users/duonghuuthanh/PycharmProjects/machinelearingapp/dataset/w2v_train_model.sav")
        else:
            sents = read_file(folder_path)
            print(len(sents))
            bigram = Phrases(sentences=sents)
            model = Word2Vec(bigram[sents], min_count=5, window=1) # sg=0 CBOW, 1 skip-gram

            Helper.cache_file(path="/Users/duonghuuthanh/PycharmProjects/machinelearingapp/dataset/w2v_train_model.sav",
                              data=model)
        return model

    @staticmethod
    def change_active_to_passive_voice(en_sentence):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(en_sentence)
        s = list(doc)
        tmp, temp, sub = "", "", -1
        for i in doc:
            if i.pos_ == 'VERB':
                s[i.i] = i
            elif i.dep_ == 'nsubj':
                sub = i.i
                temp = i
            elif i.dep_ == 'dobj':
                tmp = i.text.capitalize()
                s[i.i] = temp
                s.insert(i.i, "by")

        s[sub] = tmp
        return ' '.join(str(e) for e in s)

    @staticmethod
    def translate_syntax(sentence, src="vi", des="en"):
        k = trans.translate(sentence.replace("_", " "), src=src, dest=des)
        return ViTokenizer.tokenize(k.text)

    @staticmethod
    def translate(sentence, src="vi", des="en"):
        t1 = Translator(from_lang=src, to_lang=des)
        t2 = Translator(from_lang=des, to_lang=src)
        return ViTokenizer.tokenize(t2.translate(t1.translate(sentence.replace("_", " "))))

    # @staticmethod
    # def translate_selenium(sentence, src="vi", des="en"):
    #     driver = webdriver.Firefox(executable_path="/Users/duonghuuthanh/geckodriver")
    #     driver.get("https://translate.google.com/#view=home&op=translate&sl=%s&tl=%s" % (src, des))
    #     source = driver.find_element_by_id("source")
    #     source.send_keys(sentence)
    #     time.sleep(2)
    #     target = driver.find_element_by_class_name("tlid-translation")
    #     rs = target.text
    #     driver.quit()
    #     return rs

    @staticmethod
    def translate_selenium_2(sentences, src="vi", des="en"):
        driver = webdriver.Firefox(executable_path="/Users/duonghuuthanh/geckodriver")
        driver.get("https://translate.google.com/#view=home&op=translate&sl=%s&tl=%s" % (src, des))
        source = driver.find_element_by_id("source")
        rs = []
        for sentence in sentences:
            try:
                source.clear()
                source.send_keys(sentence)
                time.sleep(2)
                target = driver.find_element_by_class_name("tlid-translation").text
                rs.append(target)
            except:
                rs.append("")

        driver.quit()
        return rs

    @staticmethod
    def cache_file(path, data):
        f = open(path, "wb")
        pickle.dump(data, f)
        f.close()

    @staticmethod
    def load_cache_file(path_file):
        f = open(path_file, "rb")
        data = pickle.load(f)
        f.close()

        return data

    @staticmethod
    def augment_eda(sentences_dict, num=10):
        from dht.dataset.augmented.vi_senti_aug import ViSentimentAugmentation

        vi_sentences_dict = []
        for idx, sentence in enumerate(sentences_dict):
            print(idx, sentence)

            if sentence["feature"].strip() and len(sentence["feature"].strip()) > 5:
                vi = ViSentimentAugmentation(sentence=sentence["feature"])
                for _ in range(num):
                    vi_sentences_dict.append({
                        "feature": vi.synonym_replacement(),
                        "target": sentence["target"]
                    })
                    vi_sentences_dict.append({
                        "feature": vi.random_swap(),
                        "target": sentence["target"]
                    })
                    vi_sentences_dict.append({
                         "feature": vi.random_deletion(),
                         "target": sentence["target"]
                    })
                    vi_sentences_dict.append({
                         "feature": vi.random_insertion(),
                         "target": sentence["target"]
                    })

        return vi_sentences_dict

    @staticmethod
    def augment_by_w2v(sentences_dict, num=10):
        new_dict = []

        from dht.dataset.augmented.w2v_senti_aug import W2vSentimentAugmentation
        for sentence in sentences_dict:
            if sentence["feature"]:
                wv = W2vSentimentAugmentation(sentence["feature"])
                for _ in range(num):
                    new_dict.append({
                        "feature": wv.synonym_replacement(),
                        "target": sentence["target"]
                    })

        return new_dict

    @staticmethod
    def augment_by_synonym_back_trans(sentences_dict, num=20, cached_file=""):
        from dht.dataset.augmented.en_senti_aug import EnSentimentAugmentation
        des_path = "%s%s_en.sav" % (AUGMENTATION_CACHE_PATH, cached_file)

        if os.path.exists(des_path):
            en_sentences = Helper.load_cache_file(des_path)
        else:
            en_sentences = Helper.translate_selenium_2([sentence["feature"] for sentence in sentences_dict],
                                                       src="vi", des="en")

        des_path = "%s%s_synonym_back_trans.sav" % (AUGMENTATION_CACHE_PATH, cached_file)
        if os.path.exists(des_path):
            new_dict = Helper.load_cache_file(des_path)
        else:
            new_dict = []
            sentences = []
            for idx, sentence in enumerate(en_sentences):
                en = EnSentimentAugmentation(sentence=sentence)
                for _ in range(num):
                    new_sentence = en.synonym_replacement()
                    new_dict.append({
                        "feature": new_sentence,
                        "target": sentences_dict[idx]["target"]
                    })
                    sentences.append(new_sentence)

            sentences = Helper.translate_selenium_2(sentences, src="en", des="vi")

            for idx, sentence in enumerate(new_dict):
                new_dict[idx]["feature"] = ViTokenizer.tokenize(sentences[idx])

            print(new_dict)
            Helper.cache_file(des_path, data=new_dict)

        return new_dict

    @staticmethod
    def augment_by_back_translation(sentences, src="vi", des="en", cached_file=""):
        sentences = [sentence.replace("_", " ") for sentence in sentences]

        src_path = "%s%s_%s%s.sav" % (AUGMENTATION_CACHE_PATH, cached_file, des, src)
        des_path = "%s%s_%s.sav" % (AUGMENTATION_CACHE_PATH, cached_file, des)
        if os.path.exists(src_path) and os.path.exists(des_path):
            vi_sentences = Helper.load_cache_file(src_path)
        else:
            try:
                translations = trans.translate(sentences, src=src, dest=des)
                en_sentences = [t.text for t in translations]

                k = trans.translate(en_sentences, src=des, dest=src)
                vi_sentences = [ViTokenizer.tokenize(t.text) for t in k]
            except (JSONDecodeError, TypeError) as ex:
                en_sentences = Helper.translate_selenium_2(sentences, src=src, des=des)
                vi_sentences = Helper.translate_selenium_2(en_sentences, src=des, des=src)
                vi_sentences = [ViTokenizer.tokenize(t) for t in vi_sentences]

            Helper.cache_file(des_path, en_sentences)
            Helper.cache_file(src_path, vi_sentences)

        return vi_sentences

    @staticmethod
    def augment_by_syntax_tree(sentences, cached_file=""):
        sentences = [sentence.replace("_", " ") for sentence in sentences]
        try:
            en_sentences = Helper.load_cache_file("%s%s_en.sav" % (AUGMENTATION_CACHE_PATH, cached_file))
        except FileNotFoundError as ex:
            en_sentences = Helper.translate_selenium_2(sentences, src="vi", des="en")

        rs = []
        for idx, sentence in enumerate(en_sentences):
            new_sentence = []
            for sen in Helper.tokenize_sentence(sentence):
                new_sentence.append(Helper.change_active_to_passive_voice(sen))
            rs.append(' '.join(new_sentence))

        return Helper.translate_selenium_2(rs, src="en", des="vi")

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
    def tokenize_sentence(sentence):
        return sent_tokenize(sentence)

    @staticmethod
    def tokenize(source_path, destination_path):
        dirs = os.listdir(source_path)
        for d in dirs:
            if d == ".DS_Store":
                continue
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

    # @staticmethod
    # def w2v():
    #     from g


if __name__ == "__main__":
    pass
    # print(Helper.translate_selenium("Tôi rất thích Tp.HCM. Mọi người nên đến tham quan/ Tôi rất hài lòng sản phẩm đó 💩"))
    # Helper.convert_to_fasttext_data("/Users/duonghuuthanh/Desktop/My-projects/SentimentAnalysis/2018/datasettokenizednew2",
    #                                 "/Users/duonghuuthanh/PycharmProjects/machinelearingapp/dataset/vi-wordnet/fasttextdata.txt")
