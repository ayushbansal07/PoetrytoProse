import operator
import random
import numpy as np
vocab_size = 61000

PAD_ID = None
""" Reserved word ID for padding. Relict from the TensorFlow
implementation. """


GO_ID = 1
""" Reserved word ID for the start-of-sentence symbol. """


EOS_ID = 2
""" Reserved word ID for the end-of-sentence symbol. """


UNK_ID = 0
""" Reserved word ID for the unknown word (UNK). """


NOTAPPLICABLE_ID = 3
""" Reserved word ID which is currently not used. """

def loadModel():
    embeddings = []
    vocab  = []
    vocab.append('UNK')
    vocab.append('PAD')
    vocab.append('GO')
    vocab.append('EOS')
    f = open('vedas', 'r')
    i = 0

    for line in f:
        if i==0:
            i+=1
            continue
        splitLine = line.split()
        if i==1:
            i +=1
            embedding = [float(val) for val in splitLine]
            embeddings.append(np.array(embedding).reshape(100,1))
            embeddings.append(np.zeros(shape=(100, 1)))
            embeddings.append(np.ones(shape=(100, 1)))
            embeddings.append(np.ones(shape=(100, 1)) + 1.0)
            continue
        try:
            vocab.append(splitLine[0])
            embedding = [float(val) for val in splitLine[1:]]
            embeddings.append(np.array(embedding).reshape(100,1))
        except:
            continue
        i += 1
    print("Done.",len(vocab)," words loaded!")
    return vocab, embeddings


def getwv(vocab):
    f = open('data/slpAny.txt', 'r')
    f1 = open('data/wmap.txt', 'w')
    f2 = open('data/idmap.txt', 'w')
    f3 = open('data/vocab.txt', 'w')
    wmap = {}
    idmap = {}
    k = 4
    for lines in f:
        lines = lines.rstrip('\n').split()
        prose = lines[1:]
        for words in prose:
            try:
                wmap[words] = vocab.index(words)
                k += 1
            except:
                wmap[words] = vocab.index('UNK')
                # print('UNK')
    print k
    f3.write(str(vocab) + '\n')
    for keys in wmap.keys():
        f1.write(str(keys) + ' ' + str(wmap[keys]) + '\n')
    # f1.write(str(wmap) + '\n')
    return wmap

def getwordMap():

    f = open('data/slpAny.txt', 'r')
    f1 = open('data/wmap.txt', 'w')
    f2 = open('data/idmap.txt', 'w')
    f3 = open('data/vocab.txt', 'w')
    wmap = {}
    idmap = {}
    vocab = {}
    k = 4
    for lines in f:
        lines = lines.rstrip('\n').split()
        prose = lines[1:]
        for words in prose:
            if words in vocab:
                vocab[words] += 1
            else:
                vocab[words] = 1
    f.seek(0)
    sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)
    # print sorted_vocab[:1000]
    sorted_vocab = sorted_vocab[:vocab_size]
    # print len(sorted_vocab)
    vocab = {}
    # vocab.append('UNK')
    # vocab.append('<S>')
    # vocab.append('</S>')
    for words in sorted_vocab:
        vocab[words[0]] = words[1]
    # print vocab
    for lines in f:
        lines = lines.rstrip('\n').split()
        prose = lines[1:]
        for words in prose:
            if words in vocab and words not in wmap:
                wmap[words] = k
                idmap[k] = words
                k += 1
            elif words not in vocab:
                wmap[words] = UNK_ID
    for keys in wmap.keys():
        f1.write(str(keys) + ' ' + str(wmap[keys]) + '\n')
    for keys in idmap.keys():
        f2.write(str(keys) + ' ' + str(idmap[keys]) + '\n')
    for keys in vocab.keys():
        f3.write(str(keys) + '\n')
    return wmap, vocab

def clean(wmap, vocab):
    f = open('data/slpAny.txt', 'r')
    f1 = open('tokens/prose_tr_gt.txt', 'w')
    f2 = open('tokens/prose_te_gt.txt', 'w')
    f3 = open('tokens/prose_val_gt.txt', 'w')

    f4 = open('org_data/prose_tr_gt.txt', 'w')
    f5 = open('org_data/prose_te_gt.txt', 'w')
    f6 = open('org_data/prose_val_gt.txt', 'w')

    f11 = open('tokens/prose_tr_shuff.txt', 'w')
    f21 = open('tokens/prose_te_shuff.txt', 'w')
    f31 = open('tokens/prose_val_shuff.txt', 'w')

    f41 = open('org_data/prose_tr_shuff.txt', 'w')
    f51 = open('org_data/prose_te_shuff.txt', 'w')
    f61 = open('org_data/prose_val_shuff.txt', 'w')
    i = 0
    for lines in f:
        lines = lines.rstrip('\n').split()
        prose = lines[1:]
        idx_list1 = []
        for word in prose:
            idx_list1.append(wmap[word])
        for k in range(10):
            arr = prose[:]
            random.shuffle(arr)
            idx_list = []
            for word in arr:
                idx_list.append(wmap[word])

            arr = ' '.join(arr)
            prose1 = ' '.join(prose)
            if i<150000:
                f1.write(str(idx_list1) + '\n')
                f4.write(str(prose1) + '\n')
                f11.write(str(idx_list) + '\n')
                f41.write(str(arr) + '\n')
            elif i<152000:
                f3.write(str(idx_list1) + '\n')
                f6.write(str(prose1) + '\n')
                f31.write(str(idx_list) + '\n')
                f61.write(str(arr) + '\n')
            else:
                f2.write(str(idx_list1) + '\n')
                f5.write(str(prose1) + '\n')
                f21.write(str(idx_list) + '\n')
                f51.write(str(arr) + '\n')
            i += 1
    print i

# vocab, embeddings = loadModel()
# embeddings = np.array(embeddings)
# embeddings = embeddings.reshape(63192, 100)
# np.save('embeddings.npy', embeddings)

wmap, vocab = getwordMap()
print len(vocab)
print len(wmap.keys())
clean(wmap, vocab)
