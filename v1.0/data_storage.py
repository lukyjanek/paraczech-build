#!/usr/bin/env python3
# coding: utf-8

import os
import csv
import pandas as pd
from collections import defaultdict


def tag_decomposition(tag):
    nonimplicit_result = list()
    implicit_result = list()
    tag = list(tag)

    if tag[0] == 'N':
        implicit_result.append('noun')
        if tag[2] == 'M':
            implicit_result.append('m.anim')
        elif tag[2] == 'I':
            implicit_result.append('m.inan')
        elif tag[2] == 'N':
            implicit_result.append('n')
        elif tag[2] == 'F':
            implicit_result.append('f')
        if tag[4] == '1':
            nonimplicit_result.append('nom')
        elif tag[4] == '2':
            nonimplicit_result.append('gen')
        elif tag[4] == '3':
            nonimplicit_result.append('dat')
        elif tag[4] == '4':
            nonimplicit_result.append('acc')
        elif tag[4] == '5':
            nonimplicit_result.append('voc')
        elif tag[4] == '6':
            nonimplicit_result.append('loc')
        elif tag[4] == '7':
            nonimplicit_result.append('ins')
        if tag[3] == 'P':
            nonimplicit_result.append('pl')
        elif tag[3] == 'S':
            nonimplicit_result.append('sg')
        elif tag[3] == 'D':
            nonimplicit_result.append('du')

    elif tag[0] == 'A':
        implicit_result.append('adj')
        if tag[1] == 'U':
            implicit_result.append('poss')
        elif tag[1] == 'G':
            implicit_result.append('deverb:prstgr')
        elif tag[1] == 'M':
            implicit_result.append('deverb:psttgr')
        if tag[2] == 'M':
            nonimplicit_result.append('m.anim')
        elif tag[2] == 'I':
            nonimplicit_result.append('m.inan')
        elif tag[2] == 'N':
            nonimplicit_result.append('n')
        elif tag[2] == 'F':
            nonimplicit_result.append('f')
        if tag[4] == '1':
            nonimplicit_result.append('nom')
        elif tag[4] == '2':
            nonimplicit_result.append('gen')
        elif tag[4] == '3':
            nonimplicit_result.append('dat')
        elif tag[4] == '4':
            nonimplicit_result.append('acc')
        elif tag[4] == '5':
            nonimplicit_result.append('voc')
        elif tag[4] == '6':
            nonimplicit_result.append('loc')
        elif tag[4] == '7':
            nonimplicit_result.append('ins')
        if tag[3] == 'P':
            nonimplicit_result.append('pl')
        elif tag[3] == 'S':
            nonimplicit_result.append('sg')
        elif tag[3] == 'D':
            nonimplicit_result.append('du')
        if tag[5] == 'M':
            implicit_result.append('psor:m')
        elif tag[5] == 'F':
            implicit_result.append('psor:f')
        if tag[6] == 'S':
            implicit_result.append('psor:sg')
        elif tag[6] == 'P':
            implicit_result.append('psor:pl')
        if tag[9] == '1':
            nonimplicit_result.append('pstg')
        elif tag[9] == '2':
            nonimplicit_result.append('cmpg')
        elif tag[9] == '3':
            nonimplicit_result.append('sprg')
        if tag[10] == 'A':
            nonimplicit_result.append('posp')
        elif tag[10] == 'N':
            nonimplicit_result.append('negp')

    elif tag[0] == 'V':
        implicit_result.append('verb')
        if tag[1] == 'f':
            nonimplicit_result.append('inf')
        elif tag[1] == 'i':
            nonimplicit_result.append('imp')
        elif tag[1] == 'c':
            nonimplicit_result.append('cond')
        if tag[2] == 'M':
            nonimplicit_result.append('m.anim')
        elif tag[2] == 'I':
            nonimplicit_result.append('m.inan')
        elif tag[2] == 'N':
            nonimplicit_result.append('n')
        elif tag[2] == 'F':
            nonimplicit_result.append('f')
        if tag[7] == '1':
            nonimplicit_result.append('1')
        elif tag[7] == '2':
            nonimplicit_result.append('2')
        elif tag[7] == '3':
            nonimplicit_result.append('3')
        if tag[3] == 'P':
            nonimplicit_result.append('pl')
        elif tag[3] == 'S':
            nonimplicit_result.append('sg')
        elif tag[3] == 'D':
            nonimplicit_result.append('du')
        if tag[8] == 'P':
            nonimplicit_result.append('prs')
        elif tag[8] == 'R':
            nonimplicit_result.append('pst')
        elif tag[8] == 'F':
            nonimplicit_result.append('fut')
        if tag[10] == 'A':
            nonimplicit_result.append('posp')
        elif tag[10] == 'N':
            nonimplicit_result.append('negp')
        if tag[11] == 'A':
            nonimplicit_result.append('actv')
        elif tag[11] == 'P':
            nonimplicit_result.append('pass')
        if tag[12] == 'P':
            implicit_result.append('prf')
        elif tag[12] == 'I':
            implicit_result.append('ipfv')
        elif tag[12] == 'B':
            implicit_result.append('biasp')

    return '.'.join(implicit_result), '.'.join(nonimplicit_result)


def features2ud(my_tags):
        ud_mapping = {
            'noun': ('NOUN', ''),
            'adj':  ('ADJ', ''),
            'verb': ('VERB', ''),
            'm':    ('Gender', 'Masc'),
            'f':    ('Gender', 'Fem'),
            'n':    ('Gender', 'Neut'),
            'anim': ('Animacy', 'Anim'),
            'inan': ('Animacy', 'Inan'),
            'sg':   ('Number', 'Sing'),
            'pl':   ('Number', 'Plur'),
            'du':   ('Number', 'Dual'),
            'nom':  ('Case', 'Nom'),
            'gen':  ('Case', 'Gen'),
            'dat':  ('Case', 'Dat'),
            'acc':  ('Case', 'Acc'),
            'voc':  ('Case', 'Voc'),
            'loc':  ('Case', 'Loc'),
            'ins':  ('Case', 'Ins'),
            'inf':  ('VerbForm', 'Inf'),
            'imp':  ('Mood', 'Imp'),
            'cond': ('Mood', 'Cnd'),
            'prs':  ('Tense', 'Pres'),
            'pst':  ('Tense', 'Past'),
            'fut':  ('Tense', 'Fut'),
            '1':    ('Person', '1'),
            '2':    ('Person', '2'),
            '3':    ('Person', '3'),
            'actv': ('Voice', 'Act'),
            'pass': ('Voice', 'Pass'),
            'pstg': ('Degree', 'Pos'),
            'cmpg': ('Degree', 'Cmp'),
            'sprg': ('Degree', 'Sup'),
            'posp': ('Polarity', 'Pos'),
            'negp': ('Polarity', 'Neg'),
        }

        ud_pos = 'X'
        ud_feats_dict = {}
        for tag in my_tags:
            if tag in ud_mapping:
                key, val = ud_mapping[tag]
                if val is None:
                    ud_pos = key
                else:
                    ud_feats_dict[key] = val
        sorted_feats = sorted(ud_feats_dict.items())
        ud_feats_str = '|'.join([f'{k}={v}' for k, v in sorted_feats])
        if not ud_feats_str:
            ud_feats_str = '_'

        return ud_feats_str


def features2unimorph(my_tags):
    unimorph_mapping = {
        'noun': 'N',
        'adj':  'ADJ',
        'verb': 'V',
        'm': 'MASC', 'f': 'FEM', 'n': 'NEUT',
        'anim': 'ANIM', 'inan': 'INAN',
        'sg': 'SG', 'pl': 'PL', 'du': 'DU',
        'nom': 'NOM', 'gen': 'GEN', 'dat': 'DAT', 'acc': 'ACC',
        'voc': 'VOC', 'loc': 'LOC', 'ins': 'INS',
        'inf': 'NFIN', 'imp': 'IMP', 'cond': 'COND',
        'prs': 'PRS', 'pst': 'PST', 'fut': 'FUT',
        '1': '1', '2': '2', '3': '3',
        'actv': 'ACT', 'pass': 'PASS',
        'pstg': '', 'cmpg': 'CMP', 'sprg': 'SUP',
        'posp': 'POS', 'negp': 'NEG',
    }

    um_tags = []
    pos_tag = None
    for tag in my_tags:
        if tag in unimorph_mapping:
            converted = unimorph_mapping[tag]
            if converted in ['N', 'ADJ', 'V']:
                pos_tag = converted
            elif converted == '': continue
            else:
                um_tags.append(converted)
    if pos_tag:
        um_tags.insert(0, pos_tag)
    um_str = ";".join(um_tags)

    return um_str


def techlemma_decomposition(techlemma):
    parts_of_the_techlemma = techlemma.split('_')
    style_information = list()
    if '_,s' in techlemma:
        style_information.append('standard')
    if '_,a' in techlemma:
        style_information.append('archaic')
    if '_,h' in techlemma:
        style_information.append('nonstandard')
    if '_,i' in techlemma:
        style_information.append('typo')
    if '_,n' in techlemma:
        style_information.append('dialect')
    if '_,e' in techlemma:
        style_information.append('expressive')
    if '_,l' in techlemma:
        style_information.append('slang')
    if '_,v' in techlemma:
        style_information.append('vulgar')

    return parts_of_the_techlemma[0], '.'.join(style_information)


def store_data(input_folder, output_file):
    style = {
        '1': 'equal',
        '2': 'archaic',
        '3': 'archaic',
        '4': 'archaic',
        '5': 'informal',
        '6': 'informal',
        '7': 'informal',
        '8': 'informal',
        '9': 'informal',
        '-': 'normal',
    }

    graphemes = {
        'a', 'á', 'b', 'c', 'č', 'd', 'ď', 'e', 'é', 'ě', 'f', 'g', 'h', 'i',
        'í', 'j', 'k', 'l', 'm', 'n', 'ň', 'o', 'ó', 'p', 'q', 'r', 'ř', 's',
        'š', 't', 'ť', 'u', 'ú', 'ů', 'v', 'w', 'x', 'y', 'ý', 'z', 'ž'
    }

    input_files = os.listdir(input_folder)
    with open(output_file, mode='w', newline='', encoding='U8') as paradigms_file:
        csvwriter = csv.writer(paradigms_file, delimiter=',')
        # storing data
        for file_path in input_files:
            with open(input_folder + file_path, mode='r', encoding='U8') as input_file:
                for line in input_file:
                    line = line.rstrip().split('\t')
                    implicit_tag, nonimplicit_tag = tag_decomposition(line[1])
                    lemma, additional_info = techlemma_decomposition(line[0])
                    # change POS label for nouns
                    if 'noun' in implicit_tag:
                        implicit_tag = implicit_tag.replace('noun', 'noun:' + line[4].lower())
                    # skip irrelevant word forms based on tags
                    if line[1].startswith('AC') or line[1].startswith('AO') or \
                        line[1].startswith('Vc') or line[1].startswith('Vq') or \
                        line[1].startswith('Ve') or line[1].startswith('Vm') or \
                        line[1].startswith('VsY') or line[1].startswith('NNX'):
                        continue
                    # skip irrelevant words based on graphemes
                    if not graphemes.issuperset(line[2]):
                        continue
                    # store word forms
                    csvwriter.writerow(
                        [
                            '', line[0], lemma, additional_info, implicit_tag, nonimplicit_tag, 
                            line[3].replace('ň', 'ɲ').replace('kv', 'k v'), line[2], line[4].lower(),
                            line[5].lower(), 'archaic' if line[1].startswith('Vt') else style.get(line[1][14], ''),
                            line[6], str(round(float(line[7]), 10)) if len(line) == 8 else 'NA',
                            line[1]
                        ]
                    )


def make_distribution(input_file, output_folder):
    # load input file
    all_in_one = list()
    with open(input_file, mode='r', encoding='U8') as input_file:
        csvreader = csv.reader(input_file, delimiter=',')
        for line in csvreader:
            all_in_one.append(line)

    # create: forms.csv
    paradigms_header = [
        'form_id', 'lexeme', 'cell', 'phon_form', 'candidate_phon_form', 'orth_form',
        'overabundance_tag', 'UCNK', 'frequency', 'frequency_per_million'
    ]

    def get_tag_form(tag_name, info):
        if tag_name == 'overabundance_tag' and {'equal': True, 'archaic': True, 'informal': True}.get(info, False):
            return info
        return ''


    with open(output_folder + 'paraczech_forms.csv', mode='w', newline='', encoding='U8') as paradigms_file:
        csvwriter = csv.writer(paradigms_file, delimiter=',')
        csvwriter.writerow(paradigms_header)
        for idx, items in enumerate(all_in_one, start=1):
            line = [
                'f' + str(idx),
                items[2],
                items[5],
                str(items[6]) if 'borrowed' not in items[9] else '#MISSING#',
                str(items[6]) if 'borrowed' in items[9] else '',
                items[7],
                get_tag_form('overabundance_tag', items[10]),
                items[13],
                items[11],
                '0' if items[12] == 'NA' else items[12]
            ]
            csvwriter.writerow(line)

    # create: lexemes.csv
    lexemes_header = [
        'lexeme_id', 'label', 'gender', 'deverbative_transgressive',
        'possessor_gender', 'aspect', 'POS', 'name_type_tag',
        # 'origin_tag',
        'variant_tag', 'register_tag', 'epistemic_tag',
        'original_techlemma', 'frequency',
    ]

    pos_dictionary = {
        'noun:common': 'noun', 'noun:proper': 'noun', 'adj': 'adjective',
        'verb': 'verb'
    }

    def get_tag_lexeme(tag_name, info):
        if tag_name == 'variant_tag' and {'standard': True, 'dialect': True, 'slang': True}.get(info, False):
            return info
        elif tag_name == 'register_tag' and {'archaic': True, 'expressive': True, 'vulgar': True, 'nonstandard': True}.get(info, False):
            return info.replace('archaic', 'historic')
        elif tag_name == 'epistemic_tag'and {'typo': True}.get(info, False):
            return info
        return ''


    lexemes = defaultdict()
    for items in all_in_one:
        if lexemes.get(items[2], None) is None:
            inherent_features = items[4].split('.')
            lexemes[items[2]] = [
                items[2],
                items[2],
                'f' if 'f' in inherent_features else 'n' if 'n' in inherent_features else 'm.anim' if 'anim' in inherent_features else 'm.inan' if 'inan' in inherent_features else '',
                'present' if 'deverb:prstgr' in inherent_features else 'past' if 'deverb:psttgr' in inherent_features else '',
                'f' if 'psor:f' in inherent_features else 'm' if 'psor:m' in inherent_features else '',
                'prf' if 'prf' in inherent_features else 'ipfv' if 'ipfv' in inherent_features else 'biasp' if 'biasp' in inherent_features else '',
                pos_dictionary[inherent_features[0]] if 'poss' not in inherent_features else 'possessiveAdjective',
                items[8],
                # items[9],
                get_tag_lexeme('variant_tag', items[3]),
                get_tag_lexeme('register_tag', items[3]),
                get_tag_lexeme('epistemic_tag', items[3]),
                items[1],
                int(items[11])
            ]
        else:
            lexemes[items[2]][-1] += int(items[11])

    with open(output_folder + 'paraczech_lexemes.csv', mode='w', newline='', encoding='U8') as lexemes_file:
        csvwriter = csv.writer(lexemes_file, delimiter=',')
        csvwriter.writerow(lexemes_header)
        for _, items in lexemes.items():
            csvwriter.writerow(items)

    # create: cells.csv
    cells_header = [
        'cell_id', 'POS', 'ud', 'unimorph', 'frequency'
    ]

    cells = defaultdict()
    for items in all_in_one:
        if cells.get(items[5], None) is None:
            cells[items[5]] = [
                items[5],
                pos_dictionary[items[4].split('.')[0]] if 'poss' not in items[4] else 'possessiveAdjective',
                features2ud(items[5].split('.')),
                features2unimorph(items[5].split('.')),
                int(items[11])
            ]
        else:
            cells[items[5]][4] += int(items[11])

    with open(output_folder + 'paraczech_cells.csv', mode='w', newline='', encoding='U8') as cells_file:
        csvwriter = csv.writer(cells_file, delimiter=',')
        csvwriter.writerow(cells_header)
        for cells, items in cells.items():
            csvwriter.writerow(items)

    # create: sounds.csv
    sounds_header = [
        'sound_id', 'label', 'syllabic', 'long', 'consonantal', 'sonorant',
        'continuant', 'delayed release', 'approximant', 'trill', 'nasal', 'voice',
        'labial', 'round', 'labiodental', 'coronal', 'anterior', 'strident',
        'lateral', 'dorsal', 'mid', 'high', 'low', 'front', 'back'
    ]

    properties_of_sounds = {
        'a':   ['open central unrounded vowel', '1', '0', '0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0'],
        'aː':  ['long open central unrounded vowel', '1', '1', '0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0'],
        'iː':  ['long close front unrounded vowel', '1', '1', '0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0'],
        'ɪ':   ['near-close near-front unrounded vowel', '1', '0', '0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0'],
        'u':   ['close back rounded vowel', '1', '0', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '1'],
        'uː':  ['long close back rounded vowel', '1', '1', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '1'],
        'ɛ':   ['open-mid front unrounded vowel', '1', '0', '0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0'],
        'ɛː':  ['long open-mid front unrounded vowel', '1', '1', '0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0'],
        'ɔ':   ['open-mid back rounded vowel', '1', '0', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1'],
        'ɔː':  ['long open-mid back rounded vowel', '1', '1', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1'],
        'au̯': ['diphthong a-u', '0', '0', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '1'],
        'ɛu̯': ['diphthong e-u', '0', '0', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '1'],
        'ɔu̯': ['diphthong o-u', '0', '0', '0', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1'],
        'm':   ['bilabial nasal', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'm̩':   ['syllabic bilabial nasal', '1', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'ɱ':   ['labiodental nasal', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'n':   ['alveolar nasal', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
        'ɲ':   ['palatal nasal', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0'],
        'ŋ':   ['velar nasal', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
        'p':   ['voiceless bilabial plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'b':   ['voiced bilabial plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        't':   ['voiceless alveolar plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
        'd':   ['voiced alveolar plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
        'c':   ['voiceless palatal plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0'],
        'ɟ':   ['voiced palatal plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0'],
        'k':   ['voiceless velar plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
        'ɡ':   ['voiced velar plosive', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
        't͡s':  ['voiceless alveolar affricate', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
        'd͡z':  ['voiced alveolar affricate', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
        't͡ʃ':  ['voiceless postalveolar affricate', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
        'd͡ʒ':  ['voiced postalveolar affricate', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
        'f':   ['voiceless labiodental fricative', '0', '0', '1', '0', '1', '1', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'v':   ['voiced labiodental fricative', '0', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'w':   ['voiced labiodental fricative', '0', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        's':   ['voiceless alveolar sibilant', '0', '0', '1', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
        'z':   ['voiced alveolar sibilant', '0', '0', '1', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
        'ʃ':   ['voiceless postalveolar sibilant', '0', '0', '1', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1', '0', '0', '0', '0', '0', '0'],
        'ʒ':   ['voiced postalveolar sibilant', '0', '0', '1', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '1', '1', '0', '0', '0', '0', '0', '0'],
        'x':   ['voiceless velar fricative', '0', '0', '1', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
        'ɣ':   ['voiced velar fricative', '0', '0', '1', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
        'ɦ':   ['voiced glottal fricative', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'j':   ['palatal approximant', '0', '0', '0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0'],
        'l':   ['alveolar lateral approximant', '0', '0', '1', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0'],
        'l̩':   ['syllabic alveolar lateral approximant', '1', '0', '1', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0'],
        'r':   ['alveolar trill', '0', '0', '1', '1', '1', '0', '1', '1', '0', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
        'r̩':   ['syllabic alveolar trill', '1', '0', '1', '1', '1', '0', '1', '1', '0', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
        'r̝':   ['voiced raised alveolar trill', '0', '0', '1', '0', '1', '0', '1', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
        'r̝̊':  ['voiceless raised alveolar trill', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
        'ʔ':   ['glottal stop', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    }

    sounds = set()
    for items in all_in_one:
        for sound in items[6].split(' '):
            sounds.add(sound)

    with open(output_folder + 'paraczech_sounds.csv', mode='w', newline='', encoding='U8') as sounds_file:
        csvwriter = csv.writer(sounds_file, delimiter=',')
        csvwriter.writerow(sounds_header)
        for item in sounds:
            if item:
                line = [item, ]
                for p in properties_of_sounds.get(item, 26*['-']):
                    line.append(p)
                csvwriter.writerow(line)

    # create: features-values.csv
    features_header = [
        'value_id', 'label', 'feature', 'POS', 'ud', 'unimorph', 'canonical_order'
    ]

    feature_labels = {
        'noun': 'noun', 'adj': 'adjective', 'verb': 'verb', 'm': 'masculine', 'anim': 'animate',
        'inan': 'inanimate', 'f': 'feminine', 'n': 'neuter', 'pl': 'plural', 'sg': 'singular',
        'du' : 'dual', 'nom': 'nominative', 'gen': 'genitive', 'dat': 'dative', 'acc': 'acusative',
        'voc': 'vocative', 'loc': 'locative', 'ins': 'instrumental', 'poss': 'possessive',
        'psor:m': 'possession to masculine', 'psor:f': 'possession to feminine',
        'psor:sg': 'possession to singular', 'psor:pl': 'possession to plural',
        'pstg': 'positive', 'cmpg': 'comparative', 'sprg': 'superlative', 'posp': 'affirmative',
        'negp': 'negation', 'inf': 'infinitive', 'imp': 'imperative', '1': 'first person',
        '2': 'second person', '3': 'third person', 'prs': 'present', 'pst': 'past', 'fut': 'future',
        'actv': 'active', 'pass': 'passive', 'prf': 'perfective', 'ipfv': 'imperfective',
        'biasp': 'perfective and imperfective', 'cond': 'conditional',
        'deverb:prstgr': 'deverbative from present transgressive',
        'deverb:psttgr': 'deverbative from past transgressive',
    }

    feature_categories = {
        'noun': 'part-of-speech', 'adj': 'part-of-speech', 'verb': 'part-of-speech', 'm': 'gender',
        'anim': 'animacy', 'inan': 'animacy', 'f': 'gender', 'n': 'gender', 'pl': 'number',
        'sg': 'number', 'du' : 'number', 'nom': 'case', 'gen': 'case', 'dat': 'case', 'acc': 'case',
        'voc': 'case', 'loc': 'case', 'ins': 'case', 'poss': 'possessivity',
        'psor:m': 'possessivity gender', 'psor:f': 'possessivity gender',
        'psor:sg': 'possessivity number', 'psor:pl': 'possessivity number',
        'pstg': 'grade', 'cmpg': 'grade', 'sprg': 'grade', 'posp': 'polarity', 'negp': 'polarity',
        'inf': 'mood', 'imp': 'mood', '1': 'person', '2': 'person', '3': 'person',
        'prs': 'tense', 'pst': 'tense', 'fut': 'tense', 'actv': 'voice', 'pass': 'voice',
        'prf': 'aspect', 'ipfv': 'aspect', 'biasp': 'aspect', 'cond': 'mood', 'deverb:prstgr': 'transgressive',
        'deverb:psttgr': 'transgressive'
    }

    feature_pos = {
        'm': 'noun,adjective,verb', 'f': 'noun,adjective,verb', 'n': 'noun,adjective,verb', 
        'anim': 'noun', 'inan': 'noun', 'pl': 'noun,adjective,verb', 'sg': 'noun,adjective,verb', 
        'du' : 'noun,adjective,verb', 'nom': 'noun,adjective', 'gen': 'noun,adjective',
        'dat': 'noun,adjective', 'acc': 'noun,adjective', 'voc': 'noun,adjective',
        'loc': 'noun,adjective', 'ins': 'noun,adjective', 'poss': 'adjective',
        'psor:m': 'adjective', 'psor:f': 'adjective',
        'psor:sg': 'adjective', 'psor:pl': 'adjective',
        'pstg': 'adjective', 'cmpg': 'adjective', 'sprg': 'adjective', 'posp': 'noun,adjective,verb',
        'negp': 'noun,adjective,verb', 'inf': 'verb', 'imp': 'verb', '1': 'verb', '2': 'verb',
        '3': 'verb', 'prs': 'verb', 'pst': 'verb', 'fut': 'verb', 'actv': 'verb', 'pass': 'verb',
        'prf': 'verb', 'ipfv': 'verb', 'biasp': 'verb', 'cond': 'verb', 'deverb:prstgr': 'adjective',
        'deverb:psttgr': 'adjective'
    }

    feature_orders = {
        'noun': '1', 'adj': '2', 'verb': '5', 'm': '1', 'anim': '1', 'inan': '2', 'f': '2', 'n': '3',
        'pl': '2', 'sg': '1', 'du' : '3', 'nom': '1', 'gen': '2', 'dat': '3', 'acc': '4', 'voc': '5',
        'loc': '6', 'ins': '7', 'poss': '', 'psor:m': '1', 'psor:f': '2', 'psor:sg': '1', 'psor:pl': '2',
        'pstg': '1', 'cmpg': '2', 'sprg': '3', 'posp': '1', 'negp': '2', 'inf': '', 'imp': '', '1': '1',
        '2': '2', '3': '3', 'prs': '2', 'pst': '1', 'fut': '3', 'actv': '1', 'pass': '2', 'prf': '1',
        'ipfv': '2', 'biasp': '3', 'cond': '', 'deverb:prstgr': '1', 'deverb:psttgr': '2'
    }

    skip_features = [  # they are stored with lexemes, not forms
        'psor:f', 'biasp', 'poss', 'deverb:psttgr', 'ipfv',
        'psor:m', 'deverb:prstgr', 'prf'
    ]
    features = set()
    for items in all_in_one:
        for f in items[4].split('.'):
            if f in skip_features: continue
            features.add(f)
        for f in items[5].split('.'):
            if f in skip_features: continue
            features.add(f)

    with open(output_folder + 'paraczech_features-values.csv', mode='w', newline='', encoding='U8') as features_file:
        csvwriter = csv.writer(features_file, delimiter=',')
        csvwriter.writerow(features_header)
        for feature in features:
            if feature in ['noun:common', 'noun:proper', 'verb', 'adj']:
                continue
            items = [
                feature,
                feature_labels[feature],
                feature_categories[feature],
                feature_pos[feature],
                features2ud([feature,]),
                features2unimorph([feature,]),
                feature_orders[feature]
            ]
            csvwriter.writerow(items)

    # create: graphemes.csv
    graphemes_header = [
        'grapheme_id', 'grapheme_upper_case', 'canonical_order'
    ]

    graphemes = [
        'a', 'á', 'b', 'c', 'č', 'd', 'ď', 'e', 'é', 'ě', 'f', 'g', 'h', 'ch', 'i', 'í', 'j', 'k',
        'l', 'm', 'n', 'ň', 'o', 'ó', 'p', 'q', 'r', 'ř', 's', 'š', 't', 'ť', 'u', 'ú', 'ů', 'v',
        'w', 'x', 'y', 'ý', 'z', 'ž'
    ]

    with open(output_folder + 'paraczech_graphemes.csv', mode='w', newline='', encoding='U8') as graphemes_file:
        csvwriter = csv.writer(graphemes_file, delimiter=',')
        csvwriter.writerow(graphemes_header)
        for idx, grapheme in enumerate(graphemes, start=1):
            csvwriter.writerow([grapheme, grapheme.capitalize(), idx])

    # create: tags.csv
    tags_header = [
        'tag_id', 'tag_column_name', 'comment'
    ]

    tags = [
        # Overabundance
        ['equal', 'overabundance_tag', 'overabundant form relatively equal to other relevant forms'],
        ['archaic', 'overabundance_tag', 'overabundant but archaic form (less frequented)'],
        ['informal', 'overabundance_tag', 'overabundant form used in a spoken language, informal usage'],
        # Register
        ['historic', 'register_tag', 'archaic word, not contemporary, used in history'],
        ['expressive', 'register_tag', 'expressive word'],
        ['vulgar', 'register_tag', 'vulgar word'],
        ['nonstandard', 'register_tag', 'non-standard word'],
        # Usual typos
        ['typo', 'epistemic_tag', 'distortion, typo'],
        # Variants
        ['standard', 'variant_tag', 'standard word, basic form of a word, commonly used, bookish'],
        ['dialect', 'variant_tag', 'dialect'],
        ['slang', 'variant_tag', 'slang, argot'],
        # Proper deverbatives
        ['proper', 'name_type_tag', 'proper noun/adjective/verb'],
        ['common', 'name_type_tag', 'proper noun/adjective/verb'],
        # Origin
        ['borrowed', 'origin_tag', 'word adopted from other languages'],
        ['native', 'origin_tag', 'word belonging to the native lexicon'],
    ]

    with open(output_folder + 'paraczech_tags.csv', mode='w', newline='', encoding='U8') as tags_file:
        csvwriter = csv.writer(tags_file, delimiter=',')
        csvwriter.writerow(tags_header)
        csvwriter.writerows(tags)


def limit_distribution_with_threshold(input_file, output_file, threshold):
    # load input file
    all_in_one = list()
    with open(input_file, mode='r', encoding='U8') as input_file:
        csvreader = csv.reader(input_file, delimiter=',')
        for line in csvreader:
            all_in_one.append(line)
    
    # store limited version
    with open(output_file, mode='w', encoding='U8') as output_file:
        csvwriter = csv.writer(output_file, delimiter=',')
        for line in all_in_one:
            if int(line[-3]) < threshold:
                continue
            csvwriter.writerow(line)


def limit_distribution_to_lexemes_with_all_cells(input_file, output_file):
    # load input file
    all_in_one = list()
    with open(input_file, mode='r', encoding='U8') as input_file:
        csvreader = csv.reader(input_file, delimiter=',')
        for line in csvreader:
            all_in_one.append(line)
    
    # observe lexemes and their cells
    lexemes_cells = defaultdict(set)
    lexemes_entries = defaultdict(list)
    for line in all_in_one:
        lexemes_cells[line[1]].add(line[5])
        lexemes_entries[line[1]].append(line)

    # store limited version
    with open(output_file, mode='w', encoding='U8') as output_file:
        csvwriter = csv.writer(output_file, delimiter=',')
        for lexeme, cells in lexemes_cells.items():
            cells = list(cells)
            if 'noun' in lexemes_entries[lexeme][0][4] and len(cells) == 14:
                csvwriter.writerows(lexemes_entries[lexeme])
            elif 'adj' in lexemes_entries[lexeme][0][4] and len(cells) == 252:  # TODO: ?
                csvwriter.writerows(lexemes_entries[lexeme])
            elif 'verb' in lexemes_entries[lexeme][0][4] and len(cells) == 72:  # TODO: ?
                csvwriter.writerows(lexemes_entries[lexeme])


def limit_distribution_to_all_wordforms_of_lexemes_above_threshold(input_file, output_file, threshold):
    # load input file
    all_in_one = list()
    with open(input_file, mode='r', encoding='U8') as input_file:
        csvreader = csv.reader(input_file, delimiter=',')
        for line in csvreader:
            all_in_one.append(line)
    
    # sum frequencies for lexemes
    lexemes_frequencies = defaultdict(int)
    for line in all_in_one:
        lexemes_frequencies[line[1]] += int(line[-3])

    # store limited version
    with open(output_file, mode='w', encoding='U8') as output_file:
        csvwriter = csv.writer(output_file, delimiter=',')
        for line in all_in_one:
            if lexemes_frequencies[line[1]] < threshold:
                continue
            csvwriter.writerow(line)


def add_manual_corrections(input_folder, output_folder):
    for corrected_file in os.listdir(input_folder):
        for paraczech_file in os.listdir(output_folder):
            if corrected_file.split('_')[1] in paraczech_file.split('_')[1]:
                paraczech = pd.read_csv(f'{output_folder}/{paraczech_file}')
                corrections = pd.read_csv(f'{input_folder}/{corrected_file}')
                paraczech.set_index(paraczech.columns[0], inplace=True)
                corrections.set_index(corrections.columns[0], inplace=True)
                paraczech.update(corrections)
                paraczech.reset_index(inplace=True)
                paraczech.to_csv(f'{output_folder}/{paraczech_file}', index=False)
