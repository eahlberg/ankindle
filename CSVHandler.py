#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unicodecsv as csv

class CSVHandler:
    def create_csv(self, filename, words):
        f = open(filename, 'w')
        for word in words:
            f.write(word.to_csv())
        f.close()
