import re
import random

prose_file = open('data/prose_clean.bpe.txt', 'r')

f1 = open('data/vocab.txt', 'w')

f3 = open('data/src_train.txt', 'w')
f4 = open('data/dest_train.txt', 'w')

f5 = open('data/src_test.txt', 'w')
f6 = open('data/dest_test.txt', 'w')

f7 = open('data/src_val.txt', 'w')
f8 = open('data/dest_val.txt', 'w')

prose_data = prose_file.read()
prose_data = prose_data.strip()
prose_dataset = prose_data.splitlines()

src_vocab = set()
dest_vocab = set()

i = 0

for lines in prose_dataset:
    lines = lines.split(' ')
    prose = lines[1:]
    prose = [x1 for x1 in prose if x1 != '']
    idx_list1 = []
    for word in prose:
        src_vocab.add(word.strip())
    for k in range(20):
        arr = prose[:]
        random.shuffle(arr)

        arr = ' '.join(arr)
        prose1 = ' '.join(prose)
        if i<320000:
            f4.write(str(prose1) + '\n')
            f3.write(str(arr) + '\n')
        elif i<322000:
            f8.write(str(prose1) + '\n')
            f7.write(str(arr) + '\n')
        else:
            f6.write(str(prose1) + '\n')
            f5.write(str(arr) + '\n')
        i += 1
print i

for words in src_vocab:
    f1.write(words + '\n')
