#!/usr/bin/env python3

import sys
import re

from lxml import etree

import morph


if __name__ == "__main__":

    T = morph.Tagger()

    for line in sys.stdin:
        line = line.split('\t', 1)

        url = str(line[0])
        statement = line[1].split(' ')

        sentence = []
        for word in statement:
            if word.isupper():
                word = word.lower()
            word = re.sub('[^A-Za-zА-Яа-я0-9%$:\-,]+', '', word)
            if (word):
                sentence.append((word, tuple()))

        labeled = T.label(sentence)

        raw = re.sub('\n', '', line[1])
        s = etree.Element('S', URL=url, RAW=raw)

        i = 1
        for word in labeled:

            if word[2]:
                morph = '.'.join(sorted(word[2]))
            else:
                morph = ''

            if morph:
                tags = word[1] + '.' + morph
            else:
                tags = word[1]

            w = etree.SubElement(s, "W", FEAT=tags, ID=str(i))
            w.text = word[0]

            i+=1

        print(url + '\t' + etree.tostring(s, encoding='unicode'))

