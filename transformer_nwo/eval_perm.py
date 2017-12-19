from __future__ import print_function
import codecs
import os

import tensorflow as tf
import numpy as np
import operator

from hyperparams import Hyperparams as hp
from data_load import load_data, load_data_test
from data_load_perm import load_distinct_data
from train import Graph
import distance
import glob
from tqdm import tqdm
from nltk.translate.bleu_score import corpus_bleu

maplens = {}
np.random.seed(0)
def get_permuations(length):
    permutations = []
    for j in range(100):
        permutations.append(np.random.permutation(length))
    return permutations
def eval():
    # Load graph
    g = Graph(mode="test")
    print("Graph loaded")

    # Load batch
    _Y = load_distinct_data(mode="test")
    
    for i,y in enumerate(_Y):
        y = np.fromstring(y, np.int32)
        length = len(y)
        if length < 5:
            continue
        if length not in maplens:
            maplens[length] = 1
        else:
            maplens[length] += 1

    sorted_maplens = sorted(maplens.items(), key=operator.itemgetter(1),reverse=True)


    for i in range(min(len(sorted_maplens),5)):
        maxLength = sorted_maplens[i][0]
        Ydash = []

        for i,y in enumerate(_Y):
            y = np.fromstring(y, np.int32)
            if len(y) == maxLength:
                Ydash.append(_Y[i])

    
        Ydash = Ydash[:min(hp.batch_size,len(Ydash))]
        X = np.zeros((len(Ydash)*100, hp.maxlen))
        Y = np.zeros((len(Ydash)*100, hp.maxlen))
        permutations = get_permuations(maxLength)
        
        for i, y in enumerate(Ydash):
            y = np.fromstring(y, np.int32)
            for j in range(0,100):
                Y[i*100 + j][:len(y)] = y
                perm = permutations[j]
                y2 = np.zeros_like(y)
                for k in range(len(perm)):
                    y2[k] = y[perm[k]]
                X[i*100 + j][:len(y)] = y2
            
        word2idx, idx2word = g.word2idx, g.idx2word

        # Start session
        with g.graph.as_default():
            sv = tf.train.Supervisor()
            with sv.managed_session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
                # Restore parameters
                sv.saver.restore(sess, tf.train.latest_checkpoint(hp.logdir))

                # Get model
                mname = open(hp.logdir + '/checkpoint', 'r').read().split('"')[1]  # model name

                # inference
                if not os.path.exists('results_perm'): os.mkdir('results_perm')
                with codecs.open("results_perm/perm_len_{}".format(maxLength) , "w", "utf-8") as fout:
                    num_words, total_edit_distance = 0, 0
                    list_of_refs = []
                    hypotheses = []
                    for i in range(0, len(Y), hp.batch_size):
                        ### Get mini-batches
                        x = X[i:i+hp.batch_size]
                        y = Y[i:i+hp.batch_size]

                        ### Autoregressive inference
                        preds = np.zeros((hp.batch_size, hp.maxlen), np.int32)
                        for j in range(hp.maxlen):
                            _preds = sess.run(g.preds, {g.x: x, g.y: preds})
                            preds[:, j] = _preds[:, j]

                        for xx, yy, pred in zip(x, y, preds):  # sentence-wise
                            inputs = " ".join(idx2word[idx] for idx in xx).replace("_", "").strip()
                            expected = " ".join(idx2word[idx] for idx in yy).replace("_", "").strip()
                            got = " ".join(idx2word[idx] for idx in pred[:len(inputs.split())])

                            edit_distance = distance.levenshtein(expected.split(), got.split())
                            total_edit_distance += edit_distance
                            num_words += len(expected.split())

                            ref = expected.split()
                            hypothesis = got.split()

                            if len(ref) > 3 and len(hypothesis) > 3:
                                list_of_refs.append([ref])
                                hypotheses.append(hypothesis)

                            fout.write(u"Inputs  : {}\n".format(inputs))
                            fout.write(u"Expected: {}\n".format(expected))
                            fout.write(u"Got     : {}\n".format(got))
                            fout.write(u"WER     : {}\n\n".format(edit_distance))
                    try:
                        fout.write(u"Total WER: {}/{}={}\n".format(total_edit_distance,
                                                                   num_words,
                                                                round(float(total_edit_distance) / num_words, 2)))
                        score = corpus_bleu(list_of_refs, hypotheses)
                        print(score*100)
                        fout.write("Bleu Score = " + str(100*score))
                        print(round(float(total_edit_distance) / num_words, 2))
                    except:
                        pass
    
if __name__ == '__main__':
    eval()
    print("Done")
