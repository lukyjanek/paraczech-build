#!/usr/bin/env python3
# coding: utf-8

from collections import defaultdict


def merge_and_sort_words(input_path, phonetic_path, compro_path, natbor_path, freq_path, output_folder):
    # load frequencies
    frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict()))
    with open(freq_path, mode='r', encoding='U8') as freq_file:
        for line in freq_file:
            line = line.rstrip().split('\t')
            original_tuple = eval(line[0])
            frequencies[original_tuple[0]][original_tuple[1]][original_tuple[2]] = '\t'.join(line[1:])
    # merge data and sort them alphabetically
    with open(input_path, mode='r', encoding='U8') as input_file, \
         open(phonetic_path, mode='r', encoding='U8') as phonetic_file, \
         open(compro_path, mode='r', encoding='U8') as compro_file, \
         open(natbor_path, mode='r', encoding='U8') as natbor_file:
        for input_line, phonetic_line, compro_line, natbor_line in zip(input_file, phonetic_file, compro_file, natbor_file):
            merged_line = input_line.rstrip()
            merged_line += '\t' + phonetic_line.rstrip().split('\t')[-1]
            merged_line += '\t' + compro_line.rstrip().split('\t')[-1]
            merged_line += '\t' + natbor_line.rstrip().split('\t')[-1]
            mf_entry = input_line.rstrip().split('\t')
            freq = frequencies.get(mf_entry[2], {}).get(mf_entry[0].split('_')[0], {}).get(mf_entry[1], '0')
            merged_line += '\t' + freq
            # check whether the zero frequency is not caused by different tagset UCNK vs. MorfFlexCZ
            form_saved = False
            if freq == '0':
                # word form is not in the corpus
                if frequencies.get(mf_entry[2], None) is None:
                    continue
                # gender, number, case, tense ambiguity
                if any(label in mf_entry[1][2] for label in ['Y', 'Q', 'T', 'X', 'H']) or \
                   any(label in mf_entry[1][3] for label in ['W', 'X']) or \
                   any(label in mf_entry[1][4] for label in ['X']) or \
                   any(label in mf_entry[1][8] for label in ['X', 'H']):
                    d = frequencies.get(mf_entry[2], {}).get(mf_entry[0].split('_')[0], None)
                    if d is None:  # not in corpus
                        continue
                    for key in d.keys():  # unpack word forms with ambiguity
                        if key[:2] != mf_entry[1][:2]:  # skip irrelevant matches
                            continue
                        first_letter = merged_line[0]
                        form_saved = True
                        with open(output_folder + first_letter.lower() + '.tsv', mode='a', encoding='U8') as output_file:
                            new_merged_line = merged_line.rstrip('\t0').split('\t')
                            new_merged_line[1] = key
                            new_merged_line.append(d[key])
                            output_file.write('\t'.join(new_merged_line) + '\n')
            #else:  # skip word forms with non-zero frequency
            if not form_saved:
                first_letter = merged_line[0]
                with open(output_folder + first_letter.lower() + '.tsv', mode='a', encoding='U8') as output_file:
                    output_file.write(merged_line + '\n')
