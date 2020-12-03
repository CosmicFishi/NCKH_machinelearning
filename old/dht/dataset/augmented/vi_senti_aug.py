from ..utils import DatasetHelper
from .. import sentiment_stopwords, pos_list, neg_list, degree_list
from .base import AugmentationBase
from dht.helper import Helper
import random

# random.seed(1)


class ViSentimentAugmentation(AugmentationBase):
    def __init__(self, sentence):
        self.sentence = sentence

    def syntax(self):
        sentences = []

        for sen in Helper.tokenize_sentence(self.sentence):
            en_sen = Helper.translate_syntax(sen, src="vi", des="en")
            vi_sen = Helper.translate_syntax(Helper.change_active_to_passive_voice(en_sen), src="en", dest="vi")
            sentences.append(vi_sen)

        return ". ".join(sentences)

    def get_synonym_words(self, word):
        return DatasetHelper.get_synonym_words(word)

    def degree_replacement(self):
        new_words = [w for w in self.sentence.split() if w not in sentiment_stopwords]
        words = new_words.copy()

        random.shuffle(words)
        flag = False

        for i in range(len(words)):
            word = words[i]
            if word in degree_list:
                flag = True
                synonym_words = DatasetHelper.get_synonym_words(word, idx=1)
                random.seed(i)
                if len(synonym_words) > 0:
                    synonym = random.choice(synonym_words)
                    new_words = [synonym if w == word else w for w in new_words]

        new_sentence = " ".join(new_words) if flag else None

        return new_sentence

    def random_insertion(self):
        new_words = self.sentence.split()
        words = [w for w in self.sentence.split() if w in pos_list + neg_list]

        for word in words:
            synonym_words = DatasetHelper.get_synonym_words(word) if len(words) > 0 else []

            if len(synonym_words) > 0:
                new_words.insert(random.randint(0, len(new_words) - 1), synonym_words[0])

        new_sentence = " ".join(new_words)
        return new_sentence

    def shuffle(self):
        words = [w for w in self.sentence.split() if w not in sentiment_stopwords]
        random.shuffle(words)

        return " ".join(words)

    def random_deletion(self, p=0.5):
        words = self.sentence.split()
        new_words = []

        for word in words:
            t = random.uniform(0, 1)
            if t > p:
                new_words.append(word)

        if len(new_words) == 0:
            return words[random.randint(0, len(words) - 1)]

        return " ".join(new_words)

    def random_swap(self, swap_num=3):
        new_words = self.sentence.split()
        for _ in range(swap_num):
            idx1 = random.randint(0, len(new_words) - 1)
            idx2 = idx1
            while idx2 == idx1:
                idx2 = random.randint(0, len(new_words) - 1)

            new_words[idx1], new_words[idx2] = new_words[idx2], new_words[idx1]

        return " ".join(new_words)

    # def execute(self, num, eda=True):
    #     augmented_sentences = []
    #
    #     if eda:
    #         for _ in range(num):
    #             sen = self.synonym_replacement()
    #             augmented_sentences.append(sen)
    #
    #         for _ in range(num):
    #             augmented_sentences.append(self.random_swap())
    #         #
    #         # for _ in range(3):
    #         #     t = self.degree_replacement()
    #         #     if t:
    #         #         augmented_sentences.append(t)
    #
    #         for _ in range(num):
    #             augmented_sentences.append(self.random_deletion())

            # for _ in range(num):
            #     augmented_sentences.append(self.shuffle())

        # if back_trans:
        #     print("====")
        #     print(self.sentence)
        #     for _ in range(1):
        #         try:
        #             sen = self.back_translation()
        #             augmented_sentences.append(sen)
        #             print(sen)
        #             self.sentence = sen
        #         except Exception as ex:
        #             print("ERR: " + str(ex))
        #             break

        return augmented_sentences

