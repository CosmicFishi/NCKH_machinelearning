from abc import ABC, abstractmethod
from .. import sentiment_stopwords, not_list
import random


class AugmentationBase(ABC):
    def __init__(self):
        pass

    def synonym_replacement(self, replaced_num=10):
        new_words = [w for w in self.sentence.split() if w not in (sentiment_stopwords + not_list)]
        words = new_words.copy()

        random.shuffle(words)

        for i in range(min(replaced_num, len(words))):
            word = words[i]
            synonym_words = self.get_synonym_words(word)

            if len(synonym_words) > 0:
                synonym = random.choice(synonym_words)
                new_words = [synonym if w == word else w for w in new_words]

        new_sentence = " ".join(new_words)

        return new_sentence

    @abstractmethod
    def get_synonym_words(self, word):
        pass
