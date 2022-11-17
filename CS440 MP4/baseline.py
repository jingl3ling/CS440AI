"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

from argparse import _MutuallyExclusiveGroup
from doctest import Example

# def tag_to_index_lookup(tag):
#         if tag== "ADJ":
#             return 0
#         elif tag== "ADV":
#             return 1
#         elif tag== "IN":
#             return 2
#         elif tag== "PART":
#             return 3
#         elif tag== "PRON":
#             return 4
#         elif tag== "NUM":
#             return 5
#         elif tag== "CONJ":
#             return 6
#         elif tag== "UH":
#             return 7
#         elif tag== "TO":
#             return 8
#         elif tag== "VERB":
#             return 9
#         elif tag== "MODAL":
#             return 10
#         elif tag== "DET":
#             return 11
#         elif tag== "NOUN":
#             return 12
#         elif tag== "PERIOD":
#             return 13
#         elif tag== "PUNCT":
#             return 14
#         else:
#             return 15

# def index_to_tag_lookup(index):
#     if index == 0:
#         return "ADJ"
#     if index == 1:
#         return "ADV"
#     if index == 2:
#         return "IN"
#     if index == 3:
#         return "PART"
#     if index == 4:
#         return "PRON"
#     if index == 5:
#         return "NUM"
#     if index == 6:
#         return "CONJ"
#     if index == 7:
#         return "UH"
#     if index == 8:
#         return "TO"
#     if index == 9:
#         return "VERB"
#     if index == 10:
#         return "MODAL"
#     if index == 11:
#         return "DET"
#     if index == 12:
#         return "NOUN"
#     if index == 13:
#         return "PERIOD"
#     if index == 14:
#         return "PUNCT"
#     if index == 15:
#         return "X"

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words). E.g.,  [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words). E.g.,  [[word1, word2], [word3, word4]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tags={}
    tag_dict={}
    for setence in train:
        for w in setence:
                word=w[0]
                tag=w[1]
                if word not in tags:
                        tags[word]={}
                if tag not in tags[word]:
                        tags[word][tag]=1
                else:
                        tags[word][tag]+=1

                if tag not in tag_dict:
                        tag_dict[tag]=1
                else:
                        tag_dict[tag]+=1

    max_c = 0
    for tag in tag_dict:
        if tag_dict[tag]>max_c:
                max_c=tag_dict[tag]
                total_most_freq=tag

    ret = []
    for setence in test:
        curr_setence = []
        for w in setence:
                curr_word=[]
                curr_word.append(w)
                if w in tags:
                        max_count = 0
                        for tag in tags[w]:
                                if tags[w][tag]>max_count:
                                        max_count=tags[w][tag]
                                        most_freq = tag
                        curr_word.append(most_freq)
                else:
                        curr_word.append(total_most_freq)
                curr_setence.append(curr_word)
        ret.append(curr_setence)
    return ret