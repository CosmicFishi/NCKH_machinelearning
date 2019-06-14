from dht.dataset.base import BaseDataset
from .preprocess.vn_nlp import VietnameseProcess
import os


class CategoryDataset(BaseDataset):
    def __init__(self, path, **kwargs):
        super().__init__(path)
        self.is_remove_accents = kwargs.get("is_remove_accents", False)
        self.is_remove_special_character = kwargs.get("is_remove_special_character", False)
        self.is_remove_number = kwargs.get("is_remove_number", False)
        self.is_indicate_phrases = kwargs.get("is_indicate_phrases", False)
        self.is_replace_emotion_icons = kwargs.get("is_replace_emotion_icons", False)
        self.is_replace_not_terms = kwargs.get("is_replace_not_terms", False)

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
            except Exception as ex:
                print("ERROR: ", str(ex))
            else:
                sub_ds.append({
                    "feature": content,
                    "target": item
                })
            finally:
                f.close()

        return sub_ds

    def _pre_process(self, sentence):
        pre = VietnameseProcess(sentence)

        pre.replace_wrong_terms()
        pre.remove_repeated_characters()
        # pre.remove_stopwords()

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
        if self.is_remove_accents:
            pre.remove_vietnamese_accents()

        return pre.sentence

    def load_dataset_in_list(self, item):
        ds = self._read(item)

        return [d["feature"] for d in ds]
