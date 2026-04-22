#!/usr/bin/env python3
# coding: utf-8

import sys, argparse


def download_paraczech():
    return ...


def run_classifier(method):
    parser = argparse.ArgumentParser(description='Label noun classes of given Czech nouns.')
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r', encoding='utf-8'), default=sys.stdin,
                        help='Path to the input file. Reads from stdin if not provided.')
    parser.add_argument('-m', '--mode', choices=['online', 'offline', 'combined'], default='combined',
                        help='Source of morphological generation (default: combined).')
    args = parser.parse_args()

    if args.input_file.name == '<stdin>' and sys.stdin.isatty():
        parser.print_help()
        sys.exit(1)

    for line in args.input_file:
        line = line.strip()
        if line:
            print(line, *method(line, mode=args.mode), sep='\t')

    if args.input_file is not sys.stdin:
        args.input_file.close()
