from ..utils import DatasetHelper
from .. import sentiment_stopwords, pos_list, neg_list
from .base import AugmentationBase
import random

random.seed(1)


class SentimentAugmentation(AugmentationBase):
    def __init__(self, sentence):
        self.sentence = sentence

    def synonym_replacement(self, replaced_num=10):
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
        print("=== New sentence (REPLACEMENT) === ", new_sentence)

        return new_sentence

    def random_insertion(self):
        print("=== Inserting === ", self.sentence)
        new_words = self.sentence.split()
        words = [w for w in self.sentence.split() if w in pos_list + neg_list]

        # synonym_words = []
        # while len(synonym_words) < 1 and len(words) > 0:

        # word = words[0]
        for word in words:
            synonym_words = DatasetHelper.get_synonym_words(word) if len(words) > 0 else []

            if len(synonym_words) > 0:
                new_words.insert(random.randint(0, len(new_words) - 1), synonym_words[0])
                # print("=== Old sentence (INSERTION) === ", self.sentence)
                # print("=== New sentence (INSERTION) === ", new_sentence)

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

    def execute(self, num=10):
        augmented_sentences = []

        for _ in range(num):
            augmented_sentences.append(self.synonym_replacement())

        for _ in range(num):
            augmented_sentences.append(self.random_swap())

        # for _ in range(num):
        #     augmented_sentences.append(self.shuffle())

        return augmented_sentences

