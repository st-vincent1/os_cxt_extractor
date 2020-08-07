#!/bin/bash

l1=$1
l2=$2

./download.sh $l1 $l2
python extract_subs.py github $l1 $l2
python prepare_dataset.py -l $l1 $l2