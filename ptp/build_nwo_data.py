import random

f = open('bpe_data/prose.txt', 'r')
f1 = open('bpe_data_nwo/src.txt', 'w')
f2 = open('bpe_data_nwo/trg.txt', 'w')
for lines in f:
    for i in range(100):
        f2.write(lines)
    lines = lines.rstrip('\n')
    lines = lines.split()
    for i in range(100):
        x = lines
        random.shuffle(x)
        f1.write(' '.join(x) + '\n')
