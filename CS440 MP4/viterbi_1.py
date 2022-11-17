"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""

from re import T
import math
import operator


def viterbi_1(train, test):
    '''
    input:  training data (list of sentences, with tags on the words). E.g.,  [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words). E.g.,  [[word1, word2], [word3, word4]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tag_pairs={}
    tag_word={}
    tag_total={}
    word_total={}
    for sentence in train:
        #print(sentence)
        for i in range(0,len(sentence)):
                w=sentence[i]
                prev_w=sentence[i-1]
                word = w[0]
                tag = w[1]
                prev_tag=prev_w[1]
                if prev_tag not in tag_pairs:
                        tag_pairs[prev_tag]={}
                if tag not in tag_pairs[prev_tag]:
                        tag_pairs[prev_tag][tag]=1
                else:
                        tag_pairs[prev_tag][tag]+=1    

                if tag not in tag_word:
                        tag_word[tag]={}
                if word not in tag_word[tag]:
                        tag_word[tag][word]=1
                else:
                        tag_word[tag][word]+=1   

                if prev_tag=='START':
                        if prev_tag not in tag_word:
                                tag_word[prev_tag]={}
                        if prev_w not in tag_word[prev_tag]:
                                tag_word[prev_tag][prev_w]=1
                        else:
                                tag_word[prev_tag][prev_w]+=1

                if tag not in tag_total:
                        tag_total[tag]=1
                else:
                        tag_total[tag]+=1
                
                if word not in word_total:
                        word_total[word]=1
                else:
                        word_total[word]+=1

    #tag_pairs['END']={}

    tag_total_number=0
    for tag in tag_total:
        tag_total_number+=tag_total[tag]
        #print(tag)
        #print(tag_pairs[tag])

    tag_pairs_total={}
    for prev_tag in tag_pairs:
        tag_pairs_total[prev_tag]=0
        for tag in tag_pairs[prev_tag]:
                tag_pairs_total[prev_tag]+=tag_pairs[prev_tag][tag]

    tag_word_total={}
    for tag in tag_word:
        tag_word_total[tag]=0
        for word in tag_word[tag]:
                tag_word_total[tag]+=tag_word[tag][word]

    word_total_number=0
    for word in word_total:
        word_total_number+=word_total[word]

    #change to probability, smooth, and take log
    laplace=0.0001
    for prev_tag in tag_pairs:
        tag_pair_denominator=tag_pairs_total[prev_tag] + laplace*(len(tag_pairs[prev_tag])+1)  
        tag_pairs[prev_tag]['UNK']=laplace/tag_pair_denominator
        for tag in tag_pairs[prev_tag]:
                tag_pairs[prev_tag][tag]=((tag_pairs[prev_tag][tag]+laplace)/tag_pair_denominator)      
        #print(tag_pairs[prev_tag])
    for tag in tag_word:
        #print(tag)
        V=len(tag_word[tag])
        n=tag_word_total[tag]
        tag_word_denominator=n + laplace*(V+1)  
        tag_word[tag]['UNK']=laplace/tag_word_denominator
        for word in tag_word[tag]:
                tag_word[tag][word]=((tag_word[tag][word]+laplace)/tag_word_denominator) 
        # print(V)
        # print(n)
        # print(tag_word[tag])            

    #start probability
    start={}
    start['UNK']=laplace/len(tag_total)
    start['START']=1-start['UNK']
    for tag in tag_total:
        if tag != "START" and tag not in start:
                start[tag]=0

    #build viterbi
    ret=[]
    for sentence in test:
        v={}
        b={}
        v[0]={}
        b[0]={}
        word=sentence[0]
        for tag in tag_total:
                if word not in tag_word[tag]:
                        v[0][tag]=math.log(start[tag]+(laplace/(tag_pairs_total[tag] + laplace*(len(tag_pairs[tag])+1))))
                else:
                        v[0][tag]=math.log(start[tag]+tag_word[tag][word])
                b[0][tag]='START'
        for i in range(1,len(sentence)):
                v[i]={}
                b[i]={}
                word=sentence[i]
                for tagB in tag_total:
                        max_v=None
                        max_v_prev_tag=None
                        for tagA in tag_total:
                                prev_v=v[i-1][tagA]
                                if tagB not in tag_pairs[tagA]:
                                        PT=math.log(laplace/(tag_pairs_total[tagA] + laplace*(len(tag_pairs[tagA])+1)))
                                else:
                                        PT=math.log(tag_pairs[tagA][tagB])

                                if word not in tag_word[tagB]:
                                        PE=math.log(laplace/(tag_word_total[tagB] + laplace*((len(tag_word[tagB])+1))))
                                else:
                                        PE=math.log(tag_word[tagB][word])
                                curr_v=prev_v+PT+PE

                                if max_v is None:
                                        max_v=curr_v
                                        max_v_prev_tag=tagA
                                elif curr_v>max_v:
                                        max_v=curr_v
                                        max_v_prev_tag=tagA
                        v[i][tagB]=max_v
                        b[i][tagB]=max_v_prev_tag
                        # print(v[i][tagB])
                        # print(b[i][tagB])

        sentence_list=[]
        index=len(b)-1
        max_state=max(v[index].items(), key=operator.itemgetter(1))[0]
        while index>=0:
            sentence_list.append((sentence[index], max_state))
            max_state = b[index][max_state]
            index -= 1
        sentence_list.reverse()
        ret.append(sentence_list)  
    #print(ret)                      
    return ret