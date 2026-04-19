#!/usr/bin/env python3
# coding: utf-8

import lzma
import json
from collections import defaultdict
from phon_czech import ipa_czech
from recogFW import recog_foreign_word


def create_frequency_list_from_syn(input_path, output_path):
    data = defaultdict(int)
    with lzma.open(input_path, mode='rt') as input_file, \
         open(output_path, mode='w', encoding='U8') as output_file:
        for line in input_file:
            line = line.strip().split('\t')
            if len(line) >= 4:
                if line[5] in 'NAV':
                    syn_entry = (line[0].lower(), line[2], line[4])  # <- wordform, lemma, tag
                    data[syn_entry] += 1
        for key, value in data.items():
            output_file.write(
                '\t'.join(
                    [
                        str(key),
                        str(value),
                        # frequency per milion tokens
                        str(value / 4719008171 * 1000000 if value != 0 else 0)
                    ]
                ) + '\n'
            )


def extract_words_from_morfflex(input_path, output_path):
    with lzma.open(input_path, mode='rt', encoding='utf-8') as input_file, \
         open(output_path, mode='w', encoding='U8') as output_file:
        for line in input_file:
            line = line.strip().split('\t')  # -> lemma, tag, wordform
            if line[1][0] in 'ANV':  # nouns, adjectives, and verbs
                output_file.write('\t'.join(line) + '\n')


def extract_spelling_variants_from_derinet(input_path, output_path):
    database_of_ids_and_words = defaultdict()
    with open(input_path, mode='r', encoding='U8') as input_file, \
         open(output_path, mode='w', encoding='U8') as output_file:
        for line in input_file:
            line = line.strip().split('\t')
            if len(line) == 1:  # skip empty lines
                continue
            if line[3] in ['NOUN', 'ADJ', 'VERB']:
                database_of_ids_and_words[line[0]] = line[2]  # store ID and word
                if 'Type=Variant' in line[7]:  # <- spelling variant of another word
                    additional_information = json.loads(line[-1])
                    citation_form = line[2]
                    representative_variant = database_of_ids_and_words[line[6]]
                    lemma = additional_information['techlemma']
                    output_file.write(
                        '\t'.join([citation_form, representative_variant, lemma]) + '\n'
                    )


def add_phonetic_transcription(input_path, output_path):
    with open(input_path, mode='r', encoding='U8') as input_file, \
         open(output_path, mode='w', encoding='U8') as output_file:
        for line in input_file:
            line = line.strip().split('\t')
            phonetic_transcription = ipa_czech(line[-1].strip())
            output_file.write('\t'.join(line) + '\t' + phonetic_transcription + '\n')


def add_native_vs_borrowed_word(input_path, output_path, derinet_path):
    # loading DeriNet annotation
    derinet_entries_annotation = defaultdict()
    with open(derinet_path, mode='r', encoding='U8') as derinet_file:
        for line in derinet_file:
            line = line.strip().split('\t')
            if len(line) == 1:  # skip empty lines
                continue
            if line[3] in ['NOUN', 'ADJ', 'VERB']:
                if 'Loanword=True' in line[4]:  # <- borrowed word
                    additional_information = json.loads(line[-1])
                    derinet_entries_annotation[additional_information['techlemma']] = True
                else:  # <- native word
                    additional_information = json.loads(line[-1])
                    derinet_entries_annotation[additional_information['techlemma']] = False
    # final resolution
    with open(input_path, mode='r', encoding='U8') as input_file, \
         open(output_path, mode='w', encoding='U8') as output_file:
        for line in input_file:
            line = line.strip().split('\t')
            # Tool
            tool_native_vs_borrowed = recog_foreign_word(word=line[-1].strip(), pos=line[1][0])
            # DeriNet
            derinet_native_vs_borrowed = derinet_entries_annotation.get(line[0], None)
            # final decision
            if derinet_native_vs_borrowed is None:
                output_file.write(
                    '\t'.join(line) + '\tBORROWED\n' if tool_native_vs_borrowed else \
                    '\t'.join(line) + '\tNATIVE\n'
                )
            else:
                if derinet_native_vs_borrowed and tool_native_vs_borrowed:
                    output_file.write('\t'.join(line) + '\t' + 'BORROWED' + '\n')
                elif not derinet_native_vs_borrowed and not tool_native_vs_borrowed:
                    output_file.write('\t'.join(line) + '\t' + 'NATIVE' + '\n')
                elif derinet_native_vs_borrowed:
                    output_file.write('\t'.join(line) + '\t' + 'BORROWED' + '\n')
                else:
                    output_file.write('\t'.join(line) + '\t' + 'NATIVE' + '\n')


def add_common_vs_proper_word(input_path, output_path, derinet_path):
    # loading DeriNet annotation
    derinet_id2entry = defaultdict()
    derinet_child2parent = defaultdict()
    with open(derinet_path, mode='r', encoding='U8') as derinet_file:
        for line in derinet_file:
            line = line.strip().split('\t')
            if len(line) == 1:  # skip empty lines
                continue
            additional_information = json.loads(line[-1])
            derinet_id2entry[line[0]] = additional_information.get('techlemma', line[2])  # store ID and lemma
            derinet_child2parent[line[0]] = line[6]
    derinet_entry2id = defaultdict(None, [reversed(i) for i in derinet_id2entry.items()])
    # final resolution
    with open(input_path, mode='r', encoding='U8') as input_file, \
         open(output_path, mode='w', encoding='U8') as output_file:
        for line in input_file:
            line = line.strip().split('\t')
            # heuristics
            heuristics_common_vs_proper = 'PROPER' if line[-1][0].isupper() else 'COMMON'
            if heuristics_common_vs_proper == 'PROPER':
                output_file.write('\t'.join(line) + '\t' + heuristics_common_vs_proper + '\n')
                continue
            # DeriNet
            parent_id = derinet_child2parent.get(derinet_entry2id.get(line[0], None), None)
            if parent_id is None or parent_id == '':  # lemma is not found in DeriNet
                output_file.write('\t'.join(line) + '\t' + heuristics_common_vs_proper + '\n')
                continue
            while parent_id[-1] != '0':  # traversing to derivational root
                parent_id = derinet_child2parent[parent_id]
            derinet_common_vs_proper = 'PROPER' if derinet_id2entry[parent_id][0].isupper() else 'COMMON'
            output_file.write('\t'.join(line) + '\t' + derinet_common_vs_proper + '\n')
