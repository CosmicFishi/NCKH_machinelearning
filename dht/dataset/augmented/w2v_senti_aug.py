from .base import AugmentationBase
from dht.helper import Helper
import fastText


class W2vSentimentAugmentation(AugmentationBase):
    model = Helper.w2v_model()

    def __init__(self, sentence):
        self.sentence = sentence

    def get_synonym_words(self, word):
        try:
            data = W2vSentimentAugmentation.model.wv.similar_by_word(word)
            return [d[0] for d in data[:5]]
        except Exception as ex:
            # print(ex)
            return []

# class W2vSentimentAugmentation(AugmentationBase):
#     model = Helper.w2v_model()
#
#     def __init__(self, sentence):
#         self.sentence = sentence
#
#     def get_synonym_words(self, word):
#         try:
#             data = W2vSentimentAugmentation.model.wv.similar_by_word(word)
#             return [d[0] for d in data[:5]]
#         except Exception as ex:
#             # print(ex)
#             return []
