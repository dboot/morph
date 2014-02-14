""" Edit post: replace banks' names """

import re

bank_form = {'S.m.nom.sg': 'Банк',
             'S.m.gen.sg': 'Банка',
             'S.m.dat.sg': 'Банку',
             'S.m.acc.sg': 'Банк',
             'S.m.ins.sg': 'Банком',
             'S.m.prep.sg': 'Банке',

             'S.m.nom.pl': 'Банки',
             'S.m.gen.pl': 'Банков',
             'S.m.dat.pl': 'Банкам',
             'S.m.acc.pl': 'Банки',
             'S.m.ins.pl': 'Банками',
             'S.m.prep.pl': 'Банках', }

nom_pade = 'S.m.nom.sg'


def make_dict(filename='banks.txt'):
    """ Create a dict { bank name : type of word form }"""

    NAMES = {}
    p = 'Nom.sg'

    with open(filename, 'r') as bank_names:
        for line in bank_names:
            line = line.strip()
            if line is not '':
                i = line.find('S.m.')
                if nom_pade in line:
                    p = line[:i - 1].title()
                NAMES[line[:i - 1].title()] = (line[i:], p)
    return NAMES


def replace_names(post):
    """ Replace all matches with known banks' names.
        Return a tuple (Edited Post, List of tuples: (found and replaced Bank Name, Nom.sg form of bank name)).
        List has exactly the same order """

    dictio = make_dict()
    s = r'\b(' + "|".join(sorted(list(dictio.keys()), key=len, reverse=True)) + r')\b'
    pattern = re.compile(s, re.I)
    found_names = pattern.findall(post)

    for match in found_names:
        post = re.compile(r'\b' + match + r'\b').sub(bank_form[dictio[match.title()][0]], post)
    return post, [(name.title(), dictio[name.title()][1] ) for name in found_names]