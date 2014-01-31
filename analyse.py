#!/usr/bin/env python3

import morph
import sys
from lxml import etree


if __name__ == "__main__":

    T = morph.Tagger()

    for line in sys.stdin:
        line = line.split('\t', 1)

        url = line[0]
        statement = line[1].split(' ')

        sentence = []
        for word in statement:
            sentence.append((word, tuple()))

        labeled = T.label(sentence)

        s = etree.Element('s', url=url)

        i = 1
        for word in labeled:
            pos = ''
            if word[2]:
                pos = '.'.join(sorted(word[2]))

            if pos:
                tag = word[1] + '.'  + pos
            else:
                tag = word[1]

            w = etree.SubElement(s, "w", tag=tag, id=str(i))
            w.text = word[0]

            i+=1

        print(url + '\t' + etree.tostring(s, encoding='unicode').replace("\n", " "))

