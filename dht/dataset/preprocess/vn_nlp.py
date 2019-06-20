from .. import pos_list, neu_list, neg_list, not_list, degree_list, sentiment_stopwords
from . import emotion_icons, wrong_terms, s0, s1
import re


class VietnameseProcess:
    def __init__(self, sentence):
        self.sentence = sentence

    def remove_stopwords(self):
        for w in sentiment_stopwords:
            self.sentence = self.sentence.replace("%s " % w, " ")
            self.sentence = self.sentence.replace(" %s" % w, " ")

    def indicate_vietnamese_phrases(self):
        text = re.split("\s*[\s,;]\s*", self.sentence)
        length = len(text)
        for idx in range(length):
            if text[idx] in degree_list:
                if idx + 1 < length and (text[idx + 1] in pos_list):
                    text[idx] = "%s_%s" % (text[idx], text[idx + 1])
                elif idx - 1 >= 0 and (text[idx - 1] in pos_list):
                    text[idx] = "%s_%s" % (text[idx - 1], text[idx])

        self.sentence = " ".join(text)

    def replace_not_terms(self):
        text = re.split("\s*[\s,;]\s*", self.sentence)
        for idx in range(len(text)):
            if idx < len(text)-1 and text[idx] in not_list:
                if text[idx+1] in pos_list:
                    text[idx] = "notpositive"
                    text[idx+1] = ""
                if text[idx+1] in neg_list:
                    text[idx] = "notnegative"
                    text[idx+1] = ""
            elif text[idx] not in not_list:
                if text[idx] in neu_list:
                    text.append("neutral")
                elif text[idx] in pos_list:
                    text.append("positive")
                elif text[idx] in neg_list:
                    text.append("negative")

        self.sentence = " ".join(text)

    def replace_wrong_terms(self):
        for key, value in wrong_terms.items():
            if self.sentence.find(key) >= 0:
                self.sentence = self.sentence.replace(key, value)

    def replace_emotion_icons(self):
        for key, value in emotion_icons.items():
            if self.sentence.find(key) >= 0:
                self.sentence = self.sentence.replace(key, value)

    def remove_repeated_characters(self):
        self.sentence = re.sub(r'([A-Z])\1+', lambda m: m.group(1), self.sentence, flags=re.IGNORECASE)

    def remove_numbers(self):
        self.sentence = re.sub("[aj]*(ip)*\s*([0-9./])+(trieu)*(tr)*", " ", self.sentence, flags=re.IGNORECASE)

    def remove_special_character(self):
        """
        Remove all of the special characters in the sentence

        :return: the sentence after removing the special characters
        """
        punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~"""
        translator = str.maketrans(punctuation, ' '*len(punctuation))

        self.sentence = self.sentence.translate(translator)

    def remove_vietnamese_accents(self):
        """
        Remove the whole Vietnamese accents of the sentence
        Reference: https://gist.github.com/J2TEAM/9992744f15187ba51d46aecab21fd469

        :param sentence: the sentence need to remove
        :return: the sentence removed accents
        """

        result = ''
        for c in self.sentence:
            result += s0[s1.index(c)] if c in s1 else c

        self.sentence = result

