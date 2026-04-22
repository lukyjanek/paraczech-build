#!/usr/bin/env python3
# coding: utf-8

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='requests')
warnings.filterwarnings("ignore", message=".*urllib3.*")


from _get_forms import get_forms_online, get_forms_offline, get_forms_combined
from _shared_setup import download_paraczech, run_classifier


"""Label verbal class of given Czech verbs."""


def give_verb_class(lemma, mode='combined'):
    """Return verbal class."""
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
        if lemma.endswith('ovat'):
            return ('V06', '3')
        elif lemma.endswith('it'):
            return ('V02', '4')
        elif lemma.endswith(('ct', 'ci')):
            return ('V13', '1')
        elif lemma.endswith('nout'):
            if len(lemma) > 4 and lemma[-5] in 'aeiouyáéíóúýě':
                return ('V08', '2')
            return ('V09', '2')
        else:
            return ('#', '#')

    paradigm = set()
    classes = set()

    forms_3s = set()
    for t in lem:
        if t.startswith('VB-S---3P'):
            forms_3s.update(lem[t])

    past_m = set()
    for t in lem:
        if t.startswith(('VpYS', 'VpMS', 'VpIS')):
            past_m.update(lem[t])

    if not forms_3s and not past_m:
        return ('#', '#')

    imper = set()
    for t in lem:
        if t.startswith('Vi-S---2'):
            imper.update(lem[t])

    end3s = {l[-2:] for l in forms_3s} | {l[-1:] for l in forms_3s}

    # 4. GROUP (í): V02 (prosí), V03 (trpí), V04 (sází)
    if 'í' in end3s:
        past_vowels = {l[-2] for l in past_m if len(l) > 1}
        if 'i' in past_vowels and not any(v in 'eě' for v in past_vowels):
            paradigm.add('V02')
        elif any(v in 'eě' for v in past_vowels):
            if any(f.endswith(('ej', 'ěj')) for f in imper):
                paradigm.add('V04')
            else:
                paradigm.add('V03')
        elif 'i' in past_vowels and any(v in 'eě' for v in past_vowels):
            paradigm.add('V02')

    # 3. GROUP (je): V05 (kryje), V06 (kupuje)
    elif any(f.endswith('je') for f in forms_3s):
        if any(l.endswith('oval') for l in past_m):
            paradigm.add('V06')
        else:
            paradigm.add('V05')
        
    # 2. GROUP (ne): V07 (začne), V08 (mine), V09 (tiskne)
    elif (any(f.endswith(('ne', 'nou')) for f in forms_3s) and not any(f.endswith('žene') for f in forms_3s)) or lemma.endswith('jmout'):
        is_v07 = any(l.endswith(
                (
                    'al', 'ala', 'alo', 'ali', 'aly', 'el', 'ela', 'elo',
                    'eli', 'ely', 'ěl', 'ěla', 'ělo', 'ěli', 'ěly'
                )
            ) for l in past_m)
        past_stem_char = {l[-2] for l in past_m if len(l) > 1}
        if is_v07:
            paradigm.add('V07')
        else:
            has_short_past = False
            for form in past_m:
                if form.endswith('l') and len(form) > 2 and form[-2] not in 'aeiouyěáéíóúůý':
                    for f3 in forms_3s:
                        if f3.endswith('ne'):
                            stem = f3[:-2]
                            if len(stem) > 0 and stem[-1] not in 'aeiouyěáéíóúůý':
                                is_cluster = len(stem) >= 2 and stem[-2] not in 'aeiouyěáéíóúůý'
                                is_v08_process = (not is_cluster) and (stem[-1] in 'rn')
                                if is_cluster or not is_v08_process:
                                    has_short_past = True
                                    break
                    if has_short_past: break
            if has_short_past:
                paradigm.add('V09')
            else:
                paradigm.add('V08')

    # 1. GROUP (e): V10 (nese), V11 (bere), V12 (maže), V13 (peče), V14 (umře)
    elif 'e' in end3s:
        past_stem_char = {l[-2] for l in past_m if len(l) > 1}
        pres_stem_end_char = {f[-2] for f in forms_3s if len(f) > 1}
        if any(c in 'kh' for c in past_stem_char) or lemma.endswith(('ct', 'ci')):
            paradigm.add('V13')
        elif any('ře' in f for f in forms_3s) and any(l.endswith(('el', 'ela', 'elo', 'ěl', 'ěla', 'ělo')) for l in past_m):
                paradigm.add('V14')
        elif 'a' in past_stem_char and (
            any(c in 'žščřcj' for c in pres_stem_end_char) or 
            any(c in 'mpbv' for c in pres_stem_end_char)
        ):
            if any(f.endswith(('re', 'řve', 'štve')) for f in forms_3s):
                paradigm.add('V11')
            else:
                paradigm.add('V12')
        elif 'a' in past_stem_char:
            paradigm.add('V11')
        else:
            paradigm.add('V10')

    # 5. GROUP (á): V01 (dělá)
    elif any(f.endswith('á') for f in forms_3s):
        if any(l.endswith('oval') for l in past_m):
            paradigm.add('V06')
        else:
            paradigm.add('V01')

    if not paradigm:
        return ('#', '#')

    cl = {'V10': 1, 'V11': 1, 'V12': 1, 'V13': 1, 'V14': 1,
            'V09': 2, 'V08': 2, 'V07': 2,
            'V05': 3, 'V06': 3,
            'V02': 4, 'V03': 4, 'V04': 4,
            'V01': 5}
    for par in paradigm:
        classes.add(str(cl[par]))

    return ('#'.join(sorted(paradigm)), '#'.join(sorted(classes)))


# running script if it is used in shell (with stdin or path to file)
if __name__ == '__main__':
    download_paraczech()
    run_classifier(give_verb_class)
