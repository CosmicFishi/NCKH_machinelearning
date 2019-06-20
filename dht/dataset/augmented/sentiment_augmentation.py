from ..utils import DatasetHelper
from .. import sentiment_stopwords, pos_list, neg_list
from .base import AugmentationBase
import random

random.seed(1)


class SentimentAugmentation(AugmentationBase):
    def __init__(self, sentence):
        self.sentence = sentence

    def _synonym_replacement(self, replaced_num=10):
        new_words = [w for w in self.sentence.split() if w not in sentiment_stopwords]
        words = new_words.copy()

        random.shuffle(words)

        for i in range(min(replaced_num, len(words))):
            word = words[i]
            synonym_words = DatasetHelper.get_synonym_words(word)

            if len(synonym_words) > 0:
                synonym = random.choice(synonym_words)
                new_words = [synonym if w == word else w for w in new_words]

        new_sentence = " ".join(new_words)
        print("=== New sentence === ", new_sentence)

        return new_sentence

    def execute(self, num=10):
        augmented_sentences = []

        for _ in range(num):
            augmented_sentences.append(self._synonym_replacement())

        return augmented_sentences

