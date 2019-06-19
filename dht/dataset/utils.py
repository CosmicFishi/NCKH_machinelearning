from pyvi import ViTokenizer
from . import senti_wordnet, vi_wordnet


class DatasetHelper:
    @staticmethod
    def get_synonym_words(word):
        """
        words is tokenized in Vietnamese

        :param word:
        :return:
        """
        word = word.lower().strip()
        result = []
        try:
            idx = senti_wordnet["words"].index(word)
            result = [senti_wordnet["synonym_words"][idx]]
        except ValueError:
            word = " ".join(word.split("_"))
            for wordnet in vi_wordnet:
                for w in wordnet:
                    if word in w:
                        result = [r for r in w.split(", ") if r != word]
                        break
                if len(result) > 0:
                    break
        return [ViTokenizer.tokenize(w) for w in result] if len(result) > 0 else []
