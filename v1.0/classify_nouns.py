#!/usr/bin/env python3
# coding: utf-8

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='requests')
warnings.filterwarnings("ignore", message=".*urllib3.*")


from _get_forms import get_forms_online, get_forms_offline, get_forms_combined
from _shared_setup import download_paraczech, run_classifier

"""Label verbal class of given Czech nouns."""


def give_noun_class(lemma, mode='combined'):
    """Return noun class."""
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
        if lemma.endswith(('ý', 'á', 'é')):
            if lemma.endswith('ý'):
                return ('A01', 'm.anim')
            elif lemma.endswith('á'):
                return ('A01', 'f')
            elif lemma.endswith('é'):
                return ('A01', 'n')
        elif lemma.endswith('o'):
            if len(lemma) > 2 and lemma[-2] in 'aeiouyáéíóúý':
                return ('N18', 'n')
            return ('N12', 'n')
        elif lemma.endswith('í'):
            if lemma.endswith(('ní', 'tí')):
                return ('N15', 'n')
            return ('A02', '#')
        elif lemma.endswith('ost'):
            return ('N11', 'f')
        elif lemma.endswith(('us', 'os', 'es')):
            return ('N07', 'm.inam')
        elif lemma.endswith(('um', 'on')):
            return ('N16', 'n')
        elif lemma.endswith('tel'):
            return ('N02', 'm.anim')
        elif lemma.endswith(('ice', 'yně')):
            return ('N09', 'f')
        elif lemma.endswith('ista'):
            return ('N04', 'm.anim')
        elif lemma.endswith('a'):
            return ('N17', 'f')
        else:
            return ('#', '#')

    def get_ends(case_num, gender):
        tags = [t for t in lem if t.startswith(f'NN{gender}{case_num}')]
        forms = {f.lower() for t in tags for f in lem[t]}
        return {f[-1:] for f in forms}.union({f[-2:] for f in forms}).union({f[-3:] for f in forms})

    gender = list(lem.keys())[0][2]
    patterns = set()

    # Masculine Animate/Inimate
    # N01 (had), N02 (muž), N03 (soudce), N04 (táta), N05 (list), N06 (stroj), N07 (cyklus)
    if gender in ('M', 'I'):
        s2 = get_ends('S2', gender)
        s5 = get_ends('S5', gender)
        s6 = get_ends('S6', gender)

        if gender == 'M':
            if lemma.endswith('a'):
                patterns.add('N04')
            elif lemma.endswith('e'):
                patterns.add('N03')
            elif 'a' in s2 and ('e' in s5 or 'i' in s5 or 'u' in s5):
                patterns.add('N01')
            elif 'e' in s2:
                patterns.add('N02')
        else:
            if lemma.endswith('us'):
                patterns.add('N07')
            elif 'e' in s2:
                patterns.add('N06')
            elif 'a' in s2:
                patterns.add('N05')
            elif 'u' in s2:
                if 'u' in s6 or 'ě' in s6:
                    patterns.add('N05')
                elif 'e' in s6:
                    patterns.add('N05')

    # Feminine
    # N08 (žena), N09 (duše), N10 (píseň), N11 (kost)
    elif gender == 'F':
        s2 = get_ends('S2', gender)
        s5 = get_ends('S5', gender)
        p3 = get_ends('P3', gender)
        p6 = get_ends('P6', gender)

        if lemma.endswith('a') or 'o' in s5:
            if 'atu' in s2:
                patterns.add('N17')
            else:
                patterns.add('N08')
        elif lemma.endswith('e') or lemma.endswith('ě'):
            patterns.add('N09')
        elif lemma.endswith('ost') or ('i' in s2) or ('em' in p3) or ('ech' in p6):
            if lemma.endswith(('ď', 'ť', 'ň')):
                patterns.add('N10')
            else:
                patterns.add('N11')
        elif any(x in s2 for x in ['e', 'ě']) or any(x in p3 for x in ['ím', 'im']) or any(x in p6 for x in ['ích', 'ich']):
            if not lemma.endswith(('a', 'e', 'i', 'o', 'u', 'y', 'á', 'é', 'í', 'ó', 'ů', 'ú', 'ý')):
                patterns.add('N10')

    # Neuter
    # N12 (město), N13 (moře), N14 (kuře), N15 (stavení), N16 (datum), N17 (téma), N18 (rádio)
    elif gender == 'N':
        s1 = get_ends('S1', gender)
        s2 = get_ends('S2', gender)
        s3 = get_ends('S3', gender)
        s6 = get_ends('S6', gender)

        if lemma.endswith('í'):
            if 'ího' in s2 or 'ímu' in s3 or 'm' in s6:
                patterns.add('A02')
            else:
                patterns.add('N15')
        elif any(f.endswith('atu') for f in s2):
            patterns.add('N17')
        elif any(f.endswith('ete') or f.endswith('ěte') for f in s2):
            patterns.add('N14')
        elif (any(f.endswith('um') or f.endswith('on') for f in s1)) and 'a' in s2:
            patterns.add('N16')
        elif any(f.endswith(v + 'o') for v in 'aeiouy' for f in s1):
            patterns.add('N18')
        elif 'o' in s1:
            patterns.add('N12')
        elif any(f.endswith('e') or f.endswith('ě') for f in s1):
            patterns.add('N13')

    # Adjectival declension
    # A01 (mladý), A02 (jarní)
    if lemma.endswith(('ý', 'á', 'é', 'í')) and len(patterns) == 0:
        s2 = get_ends('S2', gender)

        if lemma.endswith('í'):
            patterns.add('A02')
            gender = 'Y'
        elif lemma.endswith(('ý', 'á', 'é')):
            if gender in ('M', 'I') and lemma.endswith('ý'):
                patterns.add('A01')
            elif gender == 'F' and lemma.endswith('á'):
                patterns.add('A01')
            elif gender == 'N' and lemma.endswith('é'):
                patterns.add('A01')

    if not patterns:
        return ('#', '#')

    # Gender
    gender_map = {'M': 'm.anim', 'I': 'm.inam', 'F': 'f', 'N': 'n', 'Y': 'm.anim/f'}
    gender_label = gender_map.get(gender, '#')

    return ('#'.join(patterns), gender_label)


# running script if it is used in shell (with stdin or path to file)
if __name__ == '__main__':
    download_paraczech()
    run_classifier(give_noun_class)
