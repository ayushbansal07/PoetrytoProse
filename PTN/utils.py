import re
import random
import numpy as np
import cPickle as pickle

UNK_ID = 0
PAD_ID = 1
TAG_ID = 2

vocab = set()
w2idx = {}
idx2w = {}

f = open('data/slpAny.txt', 'r')
f2 = open('data/vocab.txt', 'w')
f1 = open('data/train.txt', 'w')
f3 = open('tokens/train.txt', 'w')
f4 = open('data/test.txt', 'w')
f5 = open('tokens/test.txt', 'w')
f6 = open('data/val.txt', 'w')
f7 = open('tokens/val.txt', 'w')

f3 = open('tokens/train.txt', 'w')
f5 = open('tokens/test.txt', 'w')
f7 = open('tokens/val.txt', 'w')

for lines in f:
    lines = lines.rstrip('\n')
    sent = lines.split()
    for word in sent:
        vocab.add(word)
for words in vocab:
    f2.write(words + '\n')

vocab = list(vocab)
f.seek(0)

w2idx['PAD'] = 0
idx2w[0] = 'PAD'

i = 3
for (word) in (vocab):
    try:
        w2idx[word] = i
        idx2w[i] = word
    except:
        w2idx[word] = 1
        idx2w[1] = 'UNK'

    i+=1

j = 0
x_train = []
y_train = []
x_test = []
y_test = []
x_val = []
y_val = []
for (counter,lines) in enumerate(f):
    lines = lines.rstrip('\n')
    lines = lines.split()
    for k in range(5):
        arr = lines[1:]
        for words in arr:
            if words == ' ':
                arr.remove(words)

        # while len(arr) < 40:
        #     arr.append('PAD')
        arr = arr[:10]
        tp = []
        i = 0
        for words in arr:
            tp.append((words, i))
            i+=1

        random.shuffle(tp)
        # print len(tp)
        arr1 = []
        prose2 = []
        for words in tp:
            arr1.append(w2idx[words[0]])
            prose2.append(words[1])
        i = 0
        while len(arr1) < 10:
            arr1.append(0)
            prose2.append(len(arr1)-1)
            i+=1

        arr = ' '.join(arr)
        prose1 = ' '.join(lines[1:])

        if j < 16000:
            if len(arr1) !=len(prose2) and len(prose2)!=40:
                j += 1
                continue
            x_train.append(arr1)
            y_train.append(prose2)
            f1.write(arr+';' + prose1 + '\n')
            f3.write(str(arr1) + ';' + str(prose2) + '\n')
        elif j < 16500:
            if len(arr1) !=len(prose2):
                j += 1
                continue
            x_val.append(arr1)
            y_val.append(prose2)
            f6.write(arr+';'+prose1 + '\n')
            f7.write(str(arr1)+';'+str(prose2) + '\n')
        else:
            if len(arr1) !=len(prose2):
                j += 1
                continue
            x_test.append(arr1)
            y_test.append(prose2)
            f4.write(arr+';'+prose1 + '\n')
            f5.write(str(arr1)+';'+str(prose2) + '\n')
    j += 1

print x_train[1]
print y_train[1]
print (np.array(x_train)).shape
print (np.array(x_test)).shape
print (np.array(x_val)).shape
outdir = 'tokens/'
pickle.dump(x_train, open(outdir + "x_train.p", "wb"))
pickle.dump(x_test, open(outdir + "x_test.p", "wb"))
pickle.dump(x_val, open(outdir + "x_val.p", "wb"))
pickle.dump(y_train, open(outdir + "y_train.p", "wb"))
pickle.dump(y_test, open(outdir + "y_test.p", "wb"))
pickle.dump(y_val, open(outdir + "y_val.p", "wb"))
