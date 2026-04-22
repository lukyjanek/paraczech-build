#!/usr/bin/env python3
# coding: utf-8

import sys, csv, re
from collections import defaultdict
from _safe_request import safe_api_call


_PARACZECH_CACHE = None
_LEMMA_INDEX = None
def _load_paraczech_data(filepath='paraczech/paraczech_forms.csv'):
    """Load ParaCzech data from CSV and store them into memory."""
    global _PARACZECH_CACHE, _LEMMA_INDEX
    if _PARACZECH_CACHE is not None:
        return

    print('Info: Loading offline lexicon ParaCzech (can take some time)...', file=sys.stderr)
    
    _PARACZECH_CACHE = defaultdict(lambda: defaultdict(set))
    _LEMMA_INDEX = defaultdict(set)
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 8:
                    continue
    
                lexeme = row[1]
                orth_form = row[5]
                ucnk_tag = row[7]

                if lexeme and orth_form and ucnk_tag:
                    _PARACZECH_CACHE[lexeme][ucnk_tag].add(orth_form)
                    _LEMMA_INDEX[lexeme].add(lexeme)
                    base_lemma = re.sub(r'-\d+', '', lexeme)
                    _LEMMA_INDEX[base_lemma].add(lexeme)
                    
    except FileNotFoundError:
        print(f'Warning: File {filepath} was not found.', file=sys.stderr)
        _PARACZECH_CACHE = {}
        _LEMMA_INDEX = {}


def get_forms_online(lemma):
    """Generates word forms using the MorphoDiTa online API."""
    url = 'https://lindat.mff.cuni.cz/services/morphodita/api/generate'
    params = {'data': lemma}

    data = safe_api_call(url, params)
    if not data:
        return None

    r = data.get('result', '').strip()
    if not r:
        return None

    r = r.split('\t')
    lem = defaultdict(set)
    for i in range(0, len(r), 3):
        form = r[i]
        tag = r[i+2]
        lem[tag].add(form)

    return lem


def get_forms_offline(lemma):
    """
    Generates word forms using the offline ParaCzech dictionary.
    """
    _load_paraczech_data()
    if not _LEMMA_INDEX or lemma not in _LEMMA_INDEX:
        return None

    target_lexemes = _LEMMA_INDEX[lemma]
    lem = defaultdict(set)
    for lex in target_lexemes:
        for tag, forms in _PARACZECH_CACHE[lex].items():
            lem[tag].update(forms)

    return lem if lem else None


def get_forms_combined(lemma):
    """
    Combines offline dictionary with online API.
    """
    merged_lem = defaultdict(set)

    offline_data = get_forms_offline(lemma)
    if offline_data:
        for tag, forms in offline_data.items():
            merged_lem[tag].update(forms)

    online_data = get_forms_online(lemma)
    if online_data:
        for tag, forms in online_data.items():
            merged_lem[tag].update(forms)
            
    return merged_lem if merged_lem else None
