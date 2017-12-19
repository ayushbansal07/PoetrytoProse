from __future__ import print_function
from hyperparams import Hyperparams as hp
import numpy as np
import codecs
import re
from collections import Counter
import random
import tensorflow as tf
from data_load import load_vocab, normalize

def load_distinct_data(mode="train"):
    word2idx, idx2word = load_vocab()

    Y = []
    
    for line in codecs.open(hp.data, 'r', 'utf-8'):
        sent = line.strip().split(" ")
        sent = sent[1:]
        sent = ' '.join(sent)
        sent = normalize(sent)
        words = sent.split()

        if len(words) <= hp.maxlen:
            sent_ids = [word2idx.get(word, 0) for word in words]
            if 0 not in sent_ids: # We do not include a sentence if it has any unknown words.
                Y.append(np.array(sent_ids, np.int32).tostring())
            
    #print("###F",Y[0])
    random.shuffle(Y)
    #print("###S",Y[0])
    '''
    if mode=="train":
        Y = Y[:-hp.batch_size]
    else: # test
        Y = Y[-hp.batch_size:]
    '''
    print("# Y =", len(Y))
    return Y
