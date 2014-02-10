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


def make_dict(filename='banks.txt'):
    """ Create a dict { bank name : type of word form }"""

    NAMES = {}
    with open(filename, 'r') as bank_names:
        for line in bank_names:
            line = line.strip()
            if line is not '':
                i = line.find('S.m.')
                NAMES[line[:i - 1].title()] = line[i:]
    return NAMES


def replace_names(post):
    """ Replace all matches with known banks' names.
        Return a tuple (edited post, List of found and replaced bank names).
        List has exactly the same order """

    dictio = make_dict()
    s = "(" + "|".join(sorted(list(dictio.keys()), key=len, reverse=True)) + ")\\b"
    pattern = re.compile(s, re.I)
    found_names = pattern.findall(post)

    for match in found_names:
        post = re.compile(match).sub(bank_form[dictio[match.title()]], post)
    return post, [name.title() for name in found_names]