#!/usr/bin/env python3
# coding: utf-8

import re
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', type=str, default='../paraczech/')
parser.add_argument('--output_prefix', type=str, default='subsample')
parser.add_argument('--freq_token', type=int, default=0)
parser.add_argument('--freqPM_token', type=float, default=0)
parser.add_argument('--freq_type', type=int, default=0)
parser.add_argument('--freq_cell', type=int, default=0)
parser.add_argument('--only_nondefective_phonology', type=bool, default=False)

args = parser.parse_args()


def split_czech_word(word):
    return re.findall(r"ch|.", word)


def main():
    # load ParaCzech
    cells = pd.read_csv(f'{args.input_folder}/paraczech_cells.csv')
    forms = pd.read_csv(f'{args.input_folder}/paraczech_forms.csv')
    lexes = pd.read_csv(f'{args.input_folder}/paraczech_lexemes.csv')
    ftval = pd.read_csv(f'{args.input_folder}/paraczech_features-values.csv')
    graph = pd.read_csv(f'{args.input_folder}/paraczech_graphemes.csv')
    sound = pd.read_csv(f'{args.input_folder}/paraczech_sounds.csv')
    tagss = pd.read_csv(f'{args.input_folder}/paraczech_tags.csv')


    # process individual steps
    if args.freq_token != 0:
        forms = forms[forms.frequency >= args.freq_token]
        valid_lexeme_ids = forms['lexeme'].unique()
        lexes = lexes[lexes['lexeme_id'].isin(valid_lexeme_ids)]
        valid_cells_ids = forms['cell'].unique()
        cells = cells[cells['cell_id'].isin(valid_cells_ids)]
        used_value_ids = forms['cell'].str.split('.').explode().unique()
        ftval = ftval[ftval['value_id'].isin(used_value_ids)]
        used_sound_ids_nat = forms['phon_form'].str.split(' ').explode().unique()
        used_sound_ids_bor = forms['candidate_phon_form'].str.split(' ').explode().unique()
        used_sound_ids = pd.concat([used_sound_ids_bor, used_sound_ids_nat]).dropna().unique()
        sound = sound[sound['sound_id'].isin(used_sound_ids)]
        used_graphemes = forms['orth_form'].apply(split_czech_word).explode().unique()
        graph = graph[graph['grapheme_id'].isin(used_graphemes)]
        used_tag_ids_ove = forms['overabundance_tag'].unique()
        used_tag_ids_reg = lexes['register_tag'].unique()
        used_tag_ids_epi = lexes['epistemic_tag'].unique()
        used_tag_ids_var = lexes['variant_tag'].unique()
        used_tag_ids = pd.concat([used_tag_ids_ove, used_tag_ids_reg, used_tag_ids_epi, used_tag_ids_var]).dropna().unique()
        tagss = tagss[tagss['tag_id'].isin(used_tag_ids)]


    if args.freqPM_token != 0:
        forms = forms[forms.frequency_per_million >= args.freqPM_token]
        valid_lexeme_ids = forms['lexeme'].unique()
        lexes = lexes[lexes['lexeme_id'].isin(valid_lexeme_ids)]
        valid_cells_ids = forms['cell'].unique()
        cells = cells[cells['cell_id'].isin(valid_cells_ids)]
        used_value_ids = forms['cell'].str.split('.').explode().unique()
        ftval = ftval[ftval['value_id'].isin(used_value_ids)]
        used_sound_ids_nat = forms['phon_form'].str.split(' ').explode().unique()
        used_sound_ids_bor = forms['candidate_phon_form'].str.split(' ').explode().unique()
        used_sound_ids = pd.concat([used_sound_ids_bor, used_sound_ids_nat]).dropna().unique()
        sound = sound[sound['sound_id'].isin(used_sound_ids)]
        used_graphemes = forms['orth_form'].apply(split_czech_word).explode().unique()
        graph = graph[graph['grapheme_id'].isin(used_graphemes)]
        used_tag_ids_ove = forms['overabundance_tag'].unique()
        used_tag_ids_reg = lexes['register_tag'].unique()
        used_tag_ids_epi = lexes['epistemic_tag'].unique()
        used_tag_ids_var = lexes['variant_tag'].unique()
        used_tag_ids = pd.concat([used_tag_ids_ove, used_tag_ids_reg, used_tag_ids_epi, used_tag_ids_var]).dropna().unique()
        tagss = tagss[tagss['tag_id'].isin(used_tag_ids)]


    if args.freq_type != 0:
        lexes = lexes[lexes.frequency >= args.freq_type]
        valid_lexeme_ids = lexes['lexeme_id'].unique()
        forms = forms[forms['lexeme'].isin(valid_lexeme_ids)]
        valid_cells_ids = forms['cell'].unique()
        cells = cells[cells['cell_id'].isin(valid_cells_ids)]
        used_value_ids = forms['cell'].str.split('.').explode().unique()
        ftval = ftval[ftval['value_id'].isin(used_value_ids)]
        used_sound_ids_nat = forms['phon_form'].str.split(' ').explode().unique()
        used_sound_ids_bor = forms['candidate_phon_form'].str.split(' ').explode().unique()
        used_sound_ids = pd.concat([used_sound_ids_bor, used_sound_ids_nat]).dropna().unique()
        sound = sound[sound['sound_id'].isin(used_sound_ids)]
        used_graphemes = forms['orth_form'].apply(split_czech_word).explode().unique()
        graph = graph[graph['grapheme_id'].isin(used_graphemes)]
        used_tag_ids_ove = forms['overabundance_tag'].unique()
        used_tag_ids_reg = lexes['register_tag'].unique()
        used_tag_ids_epi = lexes['epistemic_tag'].unique()
        used_tag_ids_var = lexes['variant_tag'].unique()
        used_tag_ids = pd.concat([used_tag_ids_ove, used_tag_ids_reg, used_tag_ids_epi, used_tag_ids_var]).dropna().unique()
        tagss = tagss[tagss['tag_id'].isin(used_tag_ids)]


    if args.freq_cell != 0:
        cells = cells[cells.frequency >= args.freq_cell]
        valid_cells_ids = cells['cell_id'].unique()
        forms = forms[forms['cell'].isin(valid_cells_ids)]
        valid_lexeme_ids = forms['lexeme'].unique()
        lexes = lexes[lexes['lexeme_id'].isin(valid_lexeme_ids)]
        used_value_ids = forms['cell'].str.split('.').explode().unique()
        ftval = ftval[ftval['value_id'].isin(used_value_ids)]
        used_sound_ids_nat = forms['phon_form'].str.split(' ').explode().unique()
        used_sound_ids_bor = forms['candidate_phon_form'].str.split(' ').explode().unique()
        used_sound_ids = pd.concat([used_sound_ids_bor, used_sound_ids_nat]).dropna().unique()
        sound = sound[sound['sound_id'].isin(used_sound_ids)]
        used_graphemes = forms['orth_form'].apply(split_czech_word).explode().unique()
        graph = graph[graph['grapheme_id'].isin(used_graphemes)]
        used_tag_ids_ove = forms['overabundance_tag'].unique()
        used_tag_ids_reg = lexes['register_tag'].unique()
        used_tag_ids_epi = lexes['epistemic_tag'].unique()
        used_tag_ids_var = lexes['variant_tag'].unique()
        used_tag_ids = pd.concat([used_tag_ids_ove, used_tag_ids_reg, used_tag_ids_epi, used_tag_ids_var]).dropna().unique()
        tagss = tagss[tagss['tag_id'].isin(used_tag_ids)]


    if args.only_nondefective_phonology:
        forms = forms[forms.phon_form != '#MISSING#']
        valid_lexeme_ids = forms['lexeme'].unique()
        lexes = lexes[lexes['lexeme_id'].isin(valid_lexeme_ids)]
        valid_cells_ids = forms['cell'].unique()
        cells = cells[cells['cell_id'].isin(valid_cells_ids)]
        used_value_ids = forms['cell'].str.split('.').explode().unique()
        ftval = ftval[ftval['value_id'].isin(used_value_ids)]
        used_sound_ids_nat = forms['phon_form'].str.split(' ').explode().unique()
        used_sound_ids_bor = forms['candidate_phon_form'].str.split(' ').explode().unique()
        used_sound_ids = pd.concat([used_sound_ids_bor, used_sound_ids_nat]).dropna().unique()
        sound = sound[sound['sound_id'].isin(used_sound_ids)]
        used_graphemes = forms['orth_form'].apply(split_czech_word).explode().unique()
        graph = graph[graph['grapheme_id'].isin(used_graphemes)]
        used_tag_ids_ove = forms['overabundance_tag'].unique()
        used_tag_ids_reg = lexes['register_tag'].unique()
        used_tag_ids_epi = lexes['epistemic_tag'].unique()
        used_tag_ids_var = lexes['variant_tag'].unique()
        used_tag_ids = pd.concat([used_tag_ids_ove, used_tag_ids_reg, used_tag_ids_epi, used_tag_ids_var]).dropna().unique()
        tagss = tagss[tagss['tag_id'].isin(used_tag_ids)]


    # store resulting subsample
    cells.to_csv(f'{args.input_folder}/{args.output_prefix}_paraczech_cells.csv', index=False)
    forms.to_csv(f'{args.input_folder}/{args.output_prefix}_paraczech_forms.csv', index=False)
    lexes.to_csv(f'{args.input_folder}/{args.output_prefix}_paraczech_lexemes.csv', index=False)
    ftval.to_csv(f'{args.input_folder}/{args.output_prefix}_paraczech_features-values.csv', index=False)
    graph.to_csv(f'{args.input_folder}/{args.output_prefix}_paraczech_graphemes.csv', index=False)
    sound.to_csv(f'{args.input_folder}/{args.output_prefix}_paraczech_sounds.csv', index=False)
    tagss.to_csv(f'{args.input_folder}/{args.output_prefix}_paraczech_tags.csv', index=False)


if __name__ == '__main__':
    main()
