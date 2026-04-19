#!/usr/bin/env python3
# coding: utf-8

import os
import csv
from collections import defaultdict


def simple_statistics(input_folder):
    # features
    pos_attested = defaultdict(int)
    pos_nonattested = defaultdict(int)

    # calculate
    files = os.listdir(input_folder)
    for file in files:
        print(input_folder + file)
        with open(input_folder + file, mode='r', encoding='U8') as input_file:
            for line in input_file:
                line = line.rstrip().split('\t')
                if float(line[-1]) > 0:
                    pos_attested[line[1][0]] += 1
                else:
                    pos_nonattested[line[1][0]] += 1
    
        # print
        print(pos_attested)
        print(pos_nonattested)


def simple_statistics_above_distributions(input_folder, input_files):
    pos_order = ['commonNoun', 'properNoun', 'adjective', 'possessiveAdjective', 'verb']
    print('file', '\t'.join(pos_order), sep='\t')
    for input_file in input_files:
        pos = defaultdict(int)
        with open(input_folder + input_file, mode='r', encoding='U8') as in_file:
            csvreader = csv.reader(in_file, delimiter=',')
            for line in csvreader:
                p = line[4].split('.')[0]
                if p == 'adj' and 'poss' in line[4]:
                    pos['possessiveAdjective'] += 1
                elif p == 'adj' and 'poss' not in line[4]:
                    pos['adjective'] += 1
                elif p == 'noun:common':
                    pos['commonNoun'] += 1
                elif p == 'noun:proper':
                    pos['properNoun'] += 1
                else:
                    pos[p] += 1

        # print results
        numbers = list()
        for p in pos_order:
            numbers.append(str(pos[p]))
        print(input_file, '\t'.join(numbers), sep='\t')
