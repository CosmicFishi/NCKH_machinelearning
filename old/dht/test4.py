import re
from dht.dataset.preprocess.vn_nlp import VietnameseProcess


def remove_repeated_characters():
    def rep(obj):
        idx = obj.string.index(obj.group(0))
        if idx > 0:
            pre = VietnameseProcess(obj.string[idx - 1]).remove_vietnamese_accents()

            if obj.group(0)[0] == pre:
                return ''

        return obj.group(1)

    print(re.sub(r'([A-Z])\1+', rep, "quuuuuuá", flags=re.IGNORECASE))

def remove_repeated_punctuation():
    print(re.sub(r'((?|!|)'))

remove_repeated_characters()


# import spacy
# nlp = spacy.load('en_core_web_sm')
# doc = nlp("I love it")
# s = list(doc)
# tmp,temp,sub = "","",-1
# for i in doc:
#     if i.pos_ == 'VERB':
#         s[i.i] = i
#     elif i.dep_ == 'nsubj':
#         sub = i.i
#         temp = i
#     elif i.dep_ == 'dobj':
#         tmp = i.text.capitalize()
#         s[i.i] = temp
#         s.insert(i.i,"by")
#
# s[sub] = tmp
# print(' '.join(str(e) for e in s))