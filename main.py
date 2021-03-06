#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import DBHandler
import TranslationHandler
import WordHandler
from Word import *
import CSVHandler
import sys
import argparse
import os
import ConfigParser

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', help='Path to config file')
    args = parser.parse_args()
    configfile = args.configfile

    config = ConfigParser.ConfigParser()
    config.read(configfile)
    csvfile = str(config.get('Settings', 'csv_file'))
    kindle_db = str(config.get('Settings', 'kindle_db'))
    local_db = str(config.get('Settings', 'local_db'))
    api_key = str(config.get('Settings', 'api_key'))

    db_handler = DBHandler.DBHandler()
    if not os.path.isfile(local_db):
        db_handler.init(local_db)

    translation_handler = TranslationHandler.TranslationHandler(api_key)
    word_handler = WordHandler.WordHandler()
    csv_handler = CSVHandler.CSVHandler()

    update_local_db(kindle_db, local_db, db_handler, word_handler,
                    translation_handler)

    words = find_words_as_objects(local_db, db_handler)
    csv_handler.create_csv(csvfile, words)
    print '[main] Updated local database: %s and wrote csv to: %s' % (local_db,
                                                                csvfile)

def update_local_db(kindle_db, local_db, db_handler, word_handler, translation_handler):
    word_info = db_handler.fetch_and_insert_new_words(kindle_db, local_db)
    word_keys = word_handler.get_word_keys(word_info)
    words = word_handler.get_words(word_info)
    translations = translation_handler.translate(words)
    if translations:
        translated_words = zip(word_keys, translations)
        db_handler.insert_translations(local_db, translated_words)

def find_words_as_objects(local_db, db_handler):
    words = db_handler.fetch_all_with_translations(local_db)
    return words

if __name__ == "__main__":
    main()
