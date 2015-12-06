#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import DBHandler
import TranslationHandler
import WordHandler
from Word import *
import CSVHandler
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    # TODO: possible local db name
    parser.add_argument('csvfile', help='Name of CSV file to output')
    parser.add_argument('kindledb', help='Path to Kindle SQL database')
    parser.add_argument('apikey', help='Yandex API key')
    args = parser.parse_args()
    csvfile = args.csvfile
    kindle_db = args.kindledb
    api_key = args.apikey

    local_db = 'words.db'

    db_handler = DBHandler.DBHandler()
    translation_handler = TranslationHandler.TranslationHandler(api_key)
    word_handler = WordHandler.WordHandler()
    csv_handler = CSVHandler.CSVHandler()

    update_local_db(kindle_db, local_db, db_handler, word_handler,
                    translation_handler)

    words = find_words_as_objects(local_db, db_handler)
    csv_handler.create_csv(csvfile, words)

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
