#!/usr/bin/env python3
# coding: utf-8

import argparse
from data_extraction import create_frequency_list_from_syn, extract_words_from_morfflex, \
                            extract_spelling_variants_from_derinet, add_phonetic_transcription, \
                            add_native_vs_borrowed_word, add_common_vs_proper_word
from data_decomposition import merge_and_sort_words
from data_storage import store_data, make_distribution, \
                         limit_distribution_with_threshold, \
                         limit_distribution_to_lexemes_with_all_cells, \
                         limit_distribution_to_all_wordforms_of_lexemes_above_threshold, \
                         add_manual_corrections, add_exponents, add_inflectional_classes, \
                         delete_name_type_tag, sort_tables
from data_analysis import simple_statistics, simple_statistics_above_distributions
from collections import defaultdict
from itertools import islice


parser = argparse.ArgumentParser()
parser.add_argument('--full_pipeline', type=bool, default=False, required=False)  # takes few days if not parallelised
parser.add_argument('--extract_words_from_morfflex', type=bool, default=False, required=False)
parser.add_argument('--create_frequency_list_from_syn', type=bool, default=False, required=False)
parser.add_argument('--extract_frequencies_from_syn', type=bool, default=False, required=False)
parser.add_argument('--extract_spelling_variants_from_derinet', type=bool, default=False, required=False)
parser.add_argument('--add_phonetic_transcription', type=bool, default=False, required=False)
parser.add_argument('--add_native_vs_borrowed_word', type=bool, default=False, required=False)
parser.add_argument('--add_common_vs_proper_word', type=bool, default=False, required=False)
parser.add_argument('--merge_and_sort_words', type=bool, default=False, required=False)
parser.add_argument('--store_data', type=bool, default=False, required=False)
parser.add_argument('--make_distribution', type=bool, default=False, required=False)
# parser.add_argument('--limit_distribution_with_threshold', type=bool, default=False, required=False)
# parser.add_argument('--limit_distribution_to_lexemes_with_all_cells', type=bool, default=False, required=False)
parser.add_argument('--simple_statistics', type=bool, default=False, required=False)
parser.add_argument('--simple_statistics_above_distributions', type=bool, default=False, required=False)
parser.add_argument('--limit_distribution_to_all_wordforms_of_lexemes_above_threshold', type=bool, default=False, required=False)
parser.add_argument('--add_manual_corrections', type=bool, default=False, required=False)
parser.add_argument('--add_exponents', type=bool, default=False, required=False)
parser.add_argument('--add_inflectional_classes', type=bool, default=False, required=False)
args = parser.parse_args()


def main():
    # EXTRACTION
    ## extracting nouns, adjectives, and verbs from MorfFlexCZ
    if args.full_pipeline or args.extract_words_from_morfflex:
        extract_words_from_morfflex(
            input_path='input-resources/czech-morfflex-2.0.tsv.xz',
            output_path='extracted-annotation/from-morfflex.tsv'
        )

    ## create frequency lists from SYN v9
    ## adding frequencies per million from SYN v9
    if args.full_pipeline or args.create_frequency_list_from_syn:
        create_frequency_list_from_syn(
            input_path='input-resources/syn_v9.xz',
            output_path='extracted-annotation/frequency-list-from-syn.tsv'
        )

    # ## TODO: paralelism - extracting frequencies of wordforms in SYN v9 in bunches
    # if args.full_pipeline or args.extract_frequencies_from_syn:
    #     n_lines = 50
    #     with open('extracted-annotation/from-morfflex.tsv', mode='r', encoding='U8') as input_file, \
    #          open('extracted-annotation/frequencies-from-syn.tsv', mode='w', encoding='U8') as output_file:
    #         # loading
    #         for bunch in iter(lambda: tuple(islice(input_file, n_lines)), ()):
    #             # converting
    #             data = defaultdict(lambda: defaultdict( lambda: defaultdict(int)))
    #             for entry in bunch:
    #                 lemma, tag, wordform = entry.strip().split('\t')
    #                 data[wordform][tag][lemma] = 0
    #             # # extracting
    #             # # storing and adding frequencies per million
    #             break

    ## extracting links among spelling variants from DeriNet 2.1
    if args.full_pipeline or args.extract_spelling_variants_from_derinet:
        extract_spelling_variants_from_derinet(
            input_path='input-resources/derinet-2-1.tsv',
            output_path='extracted-annotation/spelling-vatiants.tsv'
        )



    # ADDITION
    ## distinguishing native words <em>vs.</em> borrowings
    if args.full_pipeline or args.add_native_vs_borrowed_word:
        add_native_vs_borrowed_word(
            input_path='extracted-annotation/from-morfflex.tsv',
            output_path='extracted-annotation/from-morfflex-with-natbor-annotation.tsv',
            derinet_path='input-resources/derinet-2-1.tsv'
        )

    ## distinguishing commonn nouns <em>vs.</em> proper nouns
    if args.full_pipeline or args.add_common_vs_proper_word:
        add_common_vs_proper_word(
            input_path='extracted-annotation/from-morfflex.tsv',
            output_path='extracted-annotation/from-morfflex-with-compro-annotation.tsv',
            derinet_path='input-resources/derinet-2-1.tsv'
        )

    ## adding phonetic transcriptions
    if args.full_pipeline or args.add_phonetic_transcription:
        add_phonetic_transcription(
            input_path='extracted-annotation/from-morfflex.tsv',
            output_path='extracted-annotation/from-morfflex-with-phonetic-annotation.tsv'
        )



    # DECOMPOSITION
    ## merge all extracted pieces of data about single words
    if args.full_pipeline or args.merge_and_sort_words:
        merge_and_sort_words(
            input_path = 'extracted-annotation/from-morfflex.tsv',
            output_folder = 'lists-morfflex/',
            phonetic_path = 'extracted-annotation/from-morfflex-with-phonetic-annotation.tsv',
            compro_path = 'extracted-annotation/from-morfflex-with-compro-annotation.tsv',
            natbor_path = 'extracted-annotation/from-morfflex-with-natbor-annotation.tsv',
            freq_path = 'extracted-annotation/frequency-list-from-syn.tsv'
        )



    # STORING
    ## distributing individual pieces of data together into one file - large version,
    ## transcription of individual positions of the original tag,
    ## extracting particular pieces of annotation (e.g., possessivity mark with adjectives)
    if args.full_pipeline or args.store_data:
        store_data(
            input_folder = 'lists-morfflex/',
            output_file = 'final-paraczech-package/all-in-one-1_0.csv'
        )

    # ## create limited versions of the distribution
    # if args.limit_distribution_with_threshold:
    #     limit_distribution_with_threshold(
    #         threshold=10,
    #         input_file = 'final-paraczech-package/all-in-one.csv',
    #         output_file = 'final-paraczech-package/all-in-one-limitedTR10.csv',
    #     )

    # if args.limit_distribution_to_lexemes_with_all_cells:
    #     limit_distribution_to_lexemes_with_all_cells(
    #         input_file = 'final-paraczech-package/all-in-one.csv',
    #         output_file = 'final-paraczech-package/all-in-one-limitedLAC.csv',
    #     )

    # if args.limit_distribution_to_all_wordforms_of_lexemes_above_threshold:
    #     limit_distribution_to_all_wordforms_of_lexemes_above_threshold(
    #         threshold=200,
    #         input_file = 'final-paraczech-package/all-in-one-1_0.csv',
    #         output_file = 'final-paraczech-package/all-in-one-limitedLaTR200-new.csv',
    #     )

    ## make set of files for a distribution
    if args.full_pipeline or args.make_distribution:
        make_distribution(
            input_file = 'final-paraczech-package/all-in-one-1_0.csv',
            output_folder = 'final-paraczech-package/paraczech/'
        )

    ## add manual corrections
    if args.add_manual_corrections:
        add_manual_corrections(
            input_folder = 'manual-corrections/',
            output_folder = 'final-paraczech-package/paraczech/'
        )

    ## add exponents
    if args.add_exponents:
        add_exponents(
            input_folder = 'final-paraczech-package/paraczech/',
            output_folder = 'final-paraczech-package/paraczech/',
            exponents_file = 'input-resources/exponents.csv'
        )

    ## add inflectional classes
    if args.add_inflectional_classes:
        add_inflectional_classes(
            input_folder = 'final-paraczech-package/paraczech/',
            output_folder = 'final-paraczech-package/paraczech/'
        )

    ## delete name_type_tag
    if args.delete_name_type_tag:
        delete_name_type_tag(
            input_folder = 'final-paraczech-package/paraczech/',
            output_folder = 'final-paraczech-package/paraczech/'
        )
    
    ## sort individual tables logically
    if args.sort_tables:
        sort_tables(
            input_folder = 'final-paraczech-package/paraczech/',
            output_folder = 'final-paraczech-package/paraczech/'
        )


    # STATISTICS
    if args.full_pipeline or args.simple_statistics:
        simple_statistics(
            input_folder = 'lists-morfflex/'
        )

    if args.simple_statistics_above_distributions:
        simple_statistics_above_distributions(
            input_folder = 'final-paraczech-package/',
            input_files = [
                'all-in-one-new.csv',
                # 'all-in-one-limitedLAC.csv',
                # 'all-in-one-limitedLaTR10.csv',
                # 'all-in-one-limitedLaTR50.csv',
                # 'all-in-one-limitedLaTR100.csv',
                # 'all-in-one-limitedTR10.csv',
                # 'all-in-one-limitedTR50.csv'
            ]
        )


if __name__ == '__main__':
    main()
