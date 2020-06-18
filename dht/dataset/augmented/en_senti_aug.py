from .base import AugmentationBase
#for the first time you use wordnet
#import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet


class EnSentimentAugmentation(AugmentationBase):
    def __init__(self, sentence):
        self.sentence = sentence

    def get_synonym_words(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for le in syn.lemmas():
                synonym = le.name().replace("_", " ").replace("-", " ").lower()
                synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
                synonyms.add(synonym)

        if word in synonyms:
            synonyms.remove(word)

        return list(synonyms)
