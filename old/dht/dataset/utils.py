from . import vi_wordnet, not_list, degree_list, vi_degree_wordnet

wordnets = [vi_wordnet, vi_degree_wordnet]


class DatasetHelper:
    @staticmethod
    def get_synonym_words(word, idx=0):
        """
        Get a list of synonym words of the specified word

        :param word:  words is tokenized in Vietnamese
        :param idx: words is used (0 -> normal, 1 -> vietnamese degree)
        :return:
        """
        word = word.lower().strip()
        result = []
        if word not in not_list and (idx == 1 or word not in degree_list):

            word = " ".join(word.split("_"))

            for wordnet in wordnets[idx]:
                for w in wordnet:
                    if word in w.split(", "):
                        result = [r for r in w.split(", ") if r != word]
                        break
                if len(result) > 0:
                    break

        return [w.replace(" ", "_") for w in result] if len(result) > 0 else []
