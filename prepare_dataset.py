import sys
import os
import re
import random
import argparse


def extract(input_file, idcs, train_size, dev_size, test_size, i_path, o_path):
    names = {}
    for name in ['train', 'dev', 'test']:
        names[name] = re.sub(r'^([a-z][a-z][a-z])(\.*)([a-z]*)', r'\1.{}\2\3'.format(name), input_file)
    with open(os.path.join(i_path, input_file)) as i:
        input_lines = i.readlines()
        with open(os.path.join(o_path, names['train']), 'w+') as o:
            for idx in idcs[:train_size]:
                o.write(input_lines[idx])
        with open(os.path.join(o_path, names['dev']), 'w+') as o:
            for idx in idcs[train_size: train_size + dev_size]:
                o.write(input_lines[idx])
        with open(os.path.join(o_path, names['test']), 'w+') as o:
            for idx in idcs[train_size + dev_size: train_size + dev_size + test_size]:
                o.write(input_lines[idx])
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--languages", nargs=2, help="Pair of languages as 2-letter abbreviations (e.g. de fr)")
    parser.add_argument("--train", nargs="?", type=int, default=2000000, help="Size of training data to prepare")
    parser.add_argument("--dev", nargs="?", type=int, default=10000, help="Size of development data to prepare")
    parser.add_argument("--test", nargs="?", type=int, default=10000, help="Size of test data to prepare")
    args = parser.parse_args()

    files = ('src', 'tgt', 'src.context', 'tgt.context')
    pairname = "{}-{}".format(min(args.languages[0], args.languages[1]), max(args.languages[0], args.languages[1]))
    input_path = os.path.join(os.getcwd(), 'OpenSubtitles/{}/parsed'.format(pairname))
    output_path = os.path.join(os.getcwd(), 'OpenSubtitles/{}/cxt_dataset'.format(pairname))
    population_size = args.train + args.dev + args.test
    sample_length = len(open(os.path.join(input_path, files[0])).readlines())
    # Extracting indices of random elements for training etc. from the full corpus
    indices = random.sample(range(sample_length), population_size)
    # Extracting from files
    for file in files:
        extract(file, indices, args.train, args.dev, args.test, input_path, output_path)
