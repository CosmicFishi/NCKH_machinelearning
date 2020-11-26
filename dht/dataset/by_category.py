from copyreg import pickle

from dht.dataset.augmented.vi_senti_aug import ViSentimentAugmentation
from dht.dataset.base import BaseDataset
from dht.helper import Helper
from .preprocess.vn_nlp import VietnameseProcess
import os
import pandas as pd
import random


class CategoryDataset(BaseDataset):
    def __init__(self, path, **kwargs):
        super().__init__(path)
        self.is_remove_accents = kwargs._s("is_remove_accents", False)
        self.is_remove_special_character = kwargs.get("is_remove_special_character", False)
        self.is_remove_number = kwargs.get("is_remove_number", False)
        self.is_indicate_phrases = kwargs.get("is_indicate_phrases", False)
        self.is_replace_emotion_icons = kwargs.get("is_replace_emotion_icons", False)
        self.is_replace_not_terms = kwargs.get("is_replace_not_terms", False)
        self.back_translation = kwargs.get("back_translation", False)
        self.syntax_tree = kwargs.get("syntax_tree", False)
        self.eda = kwargs.get("eda", False)
        self.synonym_trans = kwargs.get("synonym_trans", False)
        self.w2v = kwargs.get("w2v", False)

    def _read(self, item):
        """
        Read all of files in item folder
        :param item: the name of folder
        :return: a list of dictionaries has structure
        [{
            "feature": "", # the content of a file
            "target": "" # the label of feature
        }]
        """
        sub_ds = []

        item_path = "%s/%s" % (self.path, item)
        for file in os.listdir(item_path):
            file_path = "%s/%s" % (item_path, file)
            f = open(file_path, "r+", encoding="utf-8")
            try:
                content = self._pre_process(f.read())
            except:
                pass
            else:
                sub_ds = sub_ds + self._get_item(item, content)
            finally:
                f.close()

        if self.is_augmented():
            new_ds = []
            if self.back_translation:
                print("=== running back translation...")
                cached_file = self.path.split("/")[-2]
                for des in ["en", "fr", "es", "ko","ja", "th"]:#["en", "fr", "es", "ja", "ko", "th", "zh-CN"]
                    ls = Helper.augment_by_back_translation([item["feature"] for item in sub_ds], src="vi", des=des,
                                                            cached_file="%s%s" % (cached_file, item))
                    for idx, _ in enumerate(sub_ds):
                        if ls[idx]:
                            new_ds.append({
                                "feature": ls[idx].lower(),
                                "target": sub_ds[idx]["target"]
                            })
            # new expriments
            # sub_ds = sub_ds + new_ds
            # new_ds = []

            if self.syntax_tree:
                print("=== running syntax tree...")
                ls = Helper.augment_by_syntax_tree([item["feature"] for item in sub_ds],
                                                   cached_file="%s%s" % (self.path.split("/")[-2], item))
                for idx, item in enumerate(sub_ds):
                    if ls[idx]:
                        new_ds.append({
                            "feature": ls[idx].lower(),
                            "target": sub_ds[idx]["target"]
                        })

            if self.eda:
                print("=== running EDA...")
                new_ds = new_ds + Helper.augment_eda(sub_ds, num=10)

            if self.w2v:
                print("=== running W2V...")
                new_ds = new_ds + Helper.augment_by_w2v(sub_ds, num=40)

            # if self.synonym_trans:
            #     cached_file = self.path.split("/")[-2]
            #     new_ds = Helper.augment_by_synonym_back_trans(sub_ds, cached_file="%s%s" % (cached_file, item))

            sub_ds = sub_ds + new_ds

        # for item in sub_ds:
        #     item["feature"] = self._pre_process(item["feature"])

        return sub_ds

    def _get_item(self, item, content):
        return [{
            "feature": content,
            "target": item
        }]

    def _pre_process_2(self, sentence):
        pre = VietnameseProcess(sentence)

        if self.is_replace_not_terms:
            pre.replace_not_terms()
        if self.is_indicate_phrases:
            pre.indicate_vietnamese_phrases()

        return pre.sentence

    def _pre_process(self, sentence):
        pre = VietnameseProcess(sentence)

        pre.lowercase()
        pre.replace_wrong_terms()
        pre.remove_repeated_characters()
        # pre.select_postag()
        # pre.remove_stopwords()
        # pre.remove_vietnamese_accents()

        if self.is_replace_emotion_icons:
            pre.replace_emotion_icons()
        if self.is_replace_not_terms:
            pre.replace_not_terms()
        if self.is_indicate_phrases:
            pre.indicate_vietnamese_phrases()
        if self.is_remove_special_character:
            pre.remove_special_character()
        if self.is_remove_number:
            pre.remove_numbers()
        # if self.is_remove_accents:
        #     pre.remove_vietnamese_accents()

        return pre.sentence

    def is_augmented(self):
        return False

    def load_dataset_in_list(self, item):
        ds = self._read(item)

        return [d["feature"] for d in ds]


class AugmentedDataset(CategoryDataset):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)

    def is_augmented(self):
        return True

    # def _get_item(self, item, content):
    #     augmented_contents = [{
    #         "feature": content,
    #         "target": item
    #     }]
    #
    #     if content:
    #         augmented_contents = augmented_contents + [{
    #             "feature": sentence,
    #             "target": item
    #         } for sentence in ViSentimentAugmentation(content).execute(num=20, eda=False)]
    #
    #     return augmented_contents


class AugmentedValidationDataset(CategoryDataset):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)

    def _read(self, item):
        """
        Read all of files in item folder
        :param item: the name of folder
        :return: a list of dictionaries has structure
        [{
            "feature": "", # the content of a file
            "target": "" # the label of feature
        }]
        """
        sub_ds = []

        item_path = "%s/%s" % (self.path, item)
        for file in os.listdir(item_path):
            file_path = "%s/%s" % (item_path, file)
            f = open(file_path, "r+", encoding="utf-8")
            try:
                # content = self._pre_process(f.read())
                content = f.read()
            except Exception as ex:
                pass
            else:
                sub_ds = sub_ds + [{
                    "feature": content,
                    "target": item
                }]
            finally:
                f.close()

        return sub_ds

    def _get_item(self, item, content):
        return [{
            "feature": sentence,
            "target": item
        } for sentence in ViSentimentAugmentation(content).execute(num=1)] if content else []

    def load_dataset(self):
        raise Exception("Please use load_augmented_dataset method instead.")

    def load_one_class_train(self, ignore_categories=[".DS_Store"]):
        ds = []

        items = os.listdir(self.path)
        for item in items:
            if item not in ignore_categories:
                comment = self._read(item=item)
                ds.append(comment)

        ds_test = []
        ds_train = []
        for d in ds:
            #random.shuffle(d)
            c = random.choice(d)
            d.remove(c)

            ds_train += [c]
            ds_test += d

        return ds_train, ds_test

    def pre_process_one_class_train(self, ds_train, ds_test, **kwargs):
        self.is_remove_accents = kwargs.get("is_remove_accents", False)
        self.is_remove_special_character = kwargs.get("is_remove_special_character", False)
        self.is_remove_number = kwargs.get("is_remove_number", False)
        self.is_indicate_phrases = kwargs.get("is_indicate_phrases", False)
        self.is_replace_emotion_icons = kwargs.get("is_replace_emotion_icons", False)
        self.is_replace_not_terms = kwargs.get("is_replace_not_terms", False)

        for d in ds_train:
            d["feature"] = self._pre_process(d["feature"])

        for d in ds_test:
            d["feature"] = self._pre_process(d["feature"])

        return ds_train, ds_test

    def load_augmented_dataset(self, ds_train, ds_test, is_augmented=False):
        if is_augmented:
            import copy
            bk_train = copy.deepcopy(ds_train)
            for d in bk_train:
                ds_train += self._get_item(d["target"], d["feature"])

        df_train = pd.DataFrame(ds_train)
        df_test = pd.DataFrame(ds_test)

        return df_train, df_test


class AugmentedTestingDataset(CategoryDataset):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)

    def _get_item(self, item, content):
        new_sentence = ViSentimentAugmentation(content).random_insertion()

        return [{
            "feature": new_sentence,
            "target": item
        }]
