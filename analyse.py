#!/usr/bin/env python3

import sys
import re

from lxml import etree

import morph
import bank_names


if __name__ == "__main__":

    T = morph.Tagger()

    for line in sys.stdin:
        url, raw = line.split('\t', 1)

        if (re.search('\?\s*$', raw)):
            continue

        normalized = bank_names.replace_names(raw.lower())

        words = normalized[0].split(' ')

        sentence = []
        for word in words:
            if not word.istitle():
                word = word.lower()
            word = re.sub('[^A-Za-zА-Яа-я0-9\-ёъь]+', '', word)
            if (word and word not in ["-", ":", "%", "$"]):
                sentence.append((word, tuple()))

        if (sentence.__len__() > 14):
            continue

        labeled = T.label(sentence)

        s = etree.Element('S', URL=url, RAW=re.sub('\n', '', raw))

        i = 1
        has_obj = False
        for word in labeled:

            if word[2]:
                morph = '.'.join(sorted(word[2]))
            else:
                morph = ''

            if morph:
                tags = word[1] + '.' + morph
            else:
                tags = word[1]

            w = etree.SubElement(s, 'W', FEAT=tags, ID=str(i))
            if word[0].istitle():
                w.text = normalized[1].pop(0)
                w.set('OBJECT', 'true')
                has_obj = True
            else:
                w.text = word[0]

            i+=1

        if has_obj:
            print(url + '\t' + etree.tostring(s, encoding='unicode'))

        
