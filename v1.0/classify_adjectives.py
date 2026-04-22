#!/usr/bin/env python3
# coding: utf-8

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='requests')
warnings.filterwarnings("ignore", message=".*urllib3.*")


from _get_forms import get_forms_online, get_forms_offline, get_forms_combined
from _shared_setup import download_paraczech, run_classifier


"""Label verbal class of given Czech adjectives."""


def give_adjective_class(lemma, mode='combined'):
    """Return adjective class."""
    # Get forms based on selected mode
    if mode == 'online':
        lem = get_forms_online(lemma)
    elif mode == 'offline':
        lem = get_forms_offline(lemma)
    elif mode == 'combined':
        lem = get_forms_combined(lemma)
    else:
        raise ValueError(f'Unknown mode: {mode}')

    if not lem:
        if lemma.endswith('ův'):
            return ('A03', 'possessive')
        elif lemma.endswith('in'):
            return ('A04', 'possessive')
        elif lemma.endswith('í'):
            return ('A02', 'soft')
        elif lemma.endswith(('ý', 'á', 'é')):
            return ('A01', 'hard')
        else:
            return ('#', '#')

    first_tag = list(lem.keys())[0]

    adj_type = set()
    patterns = set()

    # Possessives
    # A03 (otcův), A04 (matčin)
    if first_tag.startswith('AU'):
        adj_type.add('possessive')
        all_forms = {f.lower() for t in lem for f in lem[t]}
        if lemma.endswith('ův'):
            patterns.add('A03')
        elif lemma.endswith('in'):
                patterns.add('A04')
        elif any('ův' in f for f in all_forms):
            patterns.add('A03')
        elif any('in' in f for f in all_forms):
            patterns.add('A04')
    elif lemma.endswith('ův'):
        patterns.add('A03')
    elif lemma.endswith('in'):
        patterns.add('A04')


    # Soft adjectives
    # A02 (jarní)
    elif lemma.endswith('í'):
        adj_type.add('soft')
        patterns.add('A02')

    # Hard adjectives
    # A01 (mladý)
    elif lemma.endswith(('ý', 'á', 'é')):
        adj_type.add('hard')
        patterns.add('A01')

    if not patterns:
        return ('#', '#')

    return ('#'.join(patterns), '#'.join(adj_type))


# running script if it is used in shell (with stdin or path to file)
if __name__ == '__main__':
    download_paraczech()
    run_classifier(give_adjective_class)
