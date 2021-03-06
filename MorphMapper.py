#!/usr/bin/env python3.3

import sys
import re

from lxml import etree

import morph
import bank_names


if __name__ == "__main__":

    T = morph.Tagger()

    for line in sys.stdin:
        key, value = line.split('\t', 1)

        normalized = bank_names.replace_names(value.lower())

        if (normalized[1].__len__() == 0):
            continue

        words = normalized[0].split(' ')

        sentence = []
        for word in words:
            word = re.sub('[^A-Za-zА-Яа-я0-9\-ёъь]+', '', word)
            sentence.append((word, tuple()))

        labeled = T.label(sentence)

        s = etree.Element('S', RAW=re.sub('\n', '', value))

        i = 1
        for word in labeled:

            if word[2]:
                morph = '.'.join(sorted(word[2]))
                tags = word[1] + '.' + morph
            else:
                tags = word[1]

            w = etree.SubElement(s, 'W', FEAT=tags, ID=str(i))
            if word[0].istitle():
                w.text = normalized[1][0][0]
                w.set('OBJECT', normalized[1][0][1])
                normalized[1].pop(0)
            else:
                w.text = word[0]

            i += 1

        print(key + '\t' + etree.tostring(s, encoding='unicode'))