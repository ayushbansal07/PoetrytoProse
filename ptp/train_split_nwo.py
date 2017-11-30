f1 = open('bpe_data_nwo/src.txt', 'r')
f2 = open('bpe_data_nwo/trg.txt', 'r')

f3 = open('bpe_data_nwo/src_train.txt', 'w')
f4 = open('bpe_data_nwo/trg_train.txt', 'w')

f5 = open('bpe_data_nwo/src_test.txt', 'w')
f6 = open('bpe_data_nwo/trg_test.txt', 'w')

for i, lines in enumerate(f1):
    if i<1800000:
        f3.write(lines)
    else:
        f5.write(lines)

for i, lines in enumerate(f2):
    if i<1800000:
        f4.write(lines)
    else:
        f6.write(lines)
