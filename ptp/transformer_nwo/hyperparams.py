# -*- coding: utf-8 -*-
#/usr/bin/python2

class Hyperparams:
    '''Hyperparameters'''
    # data
    source_train = '../bpe_data_nwo/src_train.txt'
    target_train = '../bpe_data_nwo/trg_train.txt'
    source_test = '../bpe_data_nwo/src_test.txt'
    target_test = '../bpe_data_nwo/trg_test.txt'
    # source_test = 'src.txt'
    # target_test = 'trg.txt'
    # training
    batch_size = 32 # alias = N
    lr = 0.0001 # learning rate. In paper, learning rate is adjusted to the global step.
    logdir = '../nwo_40' # log directory

    # model
    maxlen = 40 # Maximum number of words in a sentence. alias = T.
                # Feel free to increase this if you are ambitious.
    min_cnt = 20 # words whose occurred less than min_cnt are encoded as <UNK>.
    hidden_units = 512 # alias = C
    num_blocks = 6 # number of encoder/decoder blocks
    num_epochs = 20
    num_heads = 8
    dropout_rate = 0.1
    sinusoid = False # If True, use sinusoid. If false, positional embedding.
