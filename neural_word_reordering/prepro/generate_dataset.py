import os
import codecs
import numpy as np
import codecs
import os
from collections import Counter
import tensorflow as tf

flags = tf.flags
flags.DEFINE_string('data', '../data/preprocessed_data/', 'data directory. Should contain bpe encoded input data')
flags.DEFINE_integer('train_size', 0.8, 'training data percentage')
flags.DEFINE_integer('test_size', 0.1, 'testing data percentage')
flags.DEFINE_integer('val_size', 0.1, 'validation data percentage')
flags.DEFINE_string('mode', 'prose', 'do the generation for prose or poetry')
flags.DEFINE_integer('no_perm', 1000, 'no of permuations per data point')
FLAGS = flags.FLAGS

np.random.seed(100)

class DataGen():
    def __init__(self):
        if FLAGS.mode == 'prose':
            self.out_dir = '../data/prose/'
        else:
            self.out_dir = '../data/poetry/'
        self.inp_file = os.path.join(FLAGS.data, FLAGS.mode + '.bpe.txt')

    def jumble_words(self, data, filename):
        f1 = open(os.path.join(self.out_dir, 'src_' + filename + '.txt'), 'w')
        f2 = open(os.path.join(self.out_dir, 'trg_' + filename + '.txt'), 'w')
        for lines in data:
            for i in range(FLAGS.no_perm):
                f2.write(lines.strip() + '\n')
            word_list = lines.strip().split()
            for i in range(FLAGS.no_perm):
                np.random.shuffle(word_list)
                sent = ' '.join(word_list)
                f1.write(sent + '\n')

    def generate_data(self):
        f = open(self.inp_file, 'r')
        self.inp_data = f.read().rstrip().split('\n')
        train_size = int(FLAGS.train_size*len(self.inp_data)) + 1
        val_size = int(FLAGS.val_size*len(self.inp_data)) + 1
        train_data = self.inp_data[:train_size]
        val_data = self.inp_data[train_size:train_size+val_size]
        test_data = self.inp_data[train_size+val_size:]
        print 'Generating Permutations'
        self.jumble_words(train_data, 'train')
        print 'Train Done'
        self.jumble_words(test_data, 'test')
        print 'Test Done'
        self.jumble_words(val_data, 'val')
        print 'Val Done'

def main():
    d = DataGen()
    d.generate_data()

if __name__ == '__main__':
    main()
