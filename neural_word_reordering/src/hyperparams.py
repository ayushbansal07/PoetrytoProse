class Hyperparams:
    '''Hyperparameters'''
    # data
    source_train = '../data/prose/src_train.txt'
    target_train = '../data/prose/trg_train.txt'
    source_test = '../data/prose/src_test.txt'
    target_test = '../data/prose/trg_test.txt'
    # source_train = '../data/preprocessed_data/prose.bpe.txt'
    # target_train = '../data/preprocessed_data/prose.bpe.txt'
    # source_test = '../data/preprocessed_data/prose.bpe.txt'
    # target_test = '../data/preprocessed_data/prose.bpe.txt'
    # training
    batch_size = 32 # alias = N
    lr = 0.0001 # learning rate. In paper, learning rate is adjusted to the global step.
    logdir = '../nwo_40' # log directory

    # model
    maxlen = 40 # Maximum number of words in a sentence. alias = T.
                # Feel free to increase this if you are ambitious.
    min_cnt = 10 # words whose occurred less than min_cnt are encoded as <UNK>.
    hidden_units = 512 # alias = C
    num_blocks = 6 # number of encoder/decoder blocks
    num_epochs = 20
    num_heads = 8
    dropout_rate = 0.1
    sinusoid = False # If True, use sinusoid. If false, positional embedding.
