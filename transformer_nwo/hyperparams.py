class Hyperparams:
    '''Hyperparameters'''
    # data
    data = 'data/raw_input.bpe.txt'

    # training
    batch_size = 32 # alias = N
    lr = 0.0001 # learning rate. In paper, learning rate is adjusted to the global step.
    logdir = 'pos' # log directory

    # model
    maxlen = 40 # Maximum number of words in a sentence. alias = T.
                # Feel free to increase this if you are ambitious.
    min_cnt = 0 # words whose occurred less than min_cnt are encoded as <UNK>.
    hidden_units = 512 # alias = C
    num_blocks = 6 # number of encoder/decoder blocks
    num_epochs = 10
    num_heads = 8
    dropout_rate = 0.1
    smoothing_rate = 0.
