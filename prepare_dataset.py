import sys
import os
import random
import argparse


def extract(input_file, idcs, train_size, dev_size, test_size, path_to_parsed):
    train_name = input_file[:4] + 'train.' + input_file[4:]
    dev_name = input_file[:4] + 'dev.' + input_file[4:]
    test_name = input_file[:4] + 'test.' + input_file[4:]

    with open(os.path.join(path_to_parsed, input_file)) as i:
        input_lines = i.readlines()
        with open(train_name, 'w+') as o:
            for idx in idcs[:train_size]:
                o.write(input_lines[idx])
        with open(dev_name, 'w+') as o:
            for idx in idcs[train_size: train_size + dev_size]:
                o.write(input_lines[idx])
        with open(test_name, 'w+') as o:
            for idx in idcs[train_size + dev_size: train_size + dev_size + test_size]:
                o.write(input_lines[idx])
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", nargs="?", type=int, default=2000000, help="Size of training data to prepare")
    parser.add_argument("--dev", nargs="?", type=int, default=10000, help="Size of development data to prepare")
    parser.add_argument("--test", nargs="?", type=int, default=10000, help="Size of test data to prepare")
    parser.add_argument("-p", "--path", nargs="?", default='OpenSubtitles/parsed', help="Path to parsed subtitle data")
    args = parser.parse_args()
    # Extracted subs are in OpenSubtitles/parsed
    # Need to read that as default
    files = ['src', 'tgt', 'src.context', 'tgt.context']
    path_to_parsed = os.path.join(os.getcwd(), args.path)
    population_size = args.train + args.dev + args.test
    sample_length = len(open(os.path.join(path_to_parsed, files[0])).readlines())
    # Extracting indices of random elements for training etc. from the full corpus
    indices = random.sample(range(sample_length), population_size)
    # Extracting from files
    for file in files:
        extract(file, indices, args.train, args.dev, args.test, path_to_parsed)