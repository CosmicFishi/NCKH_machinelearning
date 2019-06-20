from pyvi import ViTokenizer
from . import senti_wordnet, vi_wordnet, not_list, degree_list


class DatasetHelper:
    @staticmethod
    def get_synonym_words(word):
        """
        Get a list of synonym words of the specified word

        :param word:  words is tokenized in Vietnamese
        :return:
        """
        word = word.lower().strip()
        result = []
        if word not in not_list and word not in degree_list:
            # try:
            #     idx = senti_wordnet["words"].index(word)
            #     result = [senti_wordnet["synonym_words"][idx]]
            # except ValueError:
            word = " ".join(word.split("_"))
            for wordnet in vi_wordnet:
                for w in wordnet:
                    if word in w.split(", "):
                        result = [r for r in w.split(", ") if r != word]
                        break
                if len(result) > 0:
                    break

        return [w.replace(" ", "_") for w in result] if len(result) > 0 else []
