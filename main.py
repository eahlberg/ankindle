#!/usr/bin/env python2

import DBHandler
import TranslationHandler
import WordHandler

# kindle_db = 'vocab_old.db'
kindle_db = '/Volumes/Kindle/system/vocabulary/vocab.db'
local_db = 'words.db'

db_handler = DBHandler.DBHandler()
translation_handler = TranslationHandler.TranslationHandler()
word_handler = WordHandler.WordHandler()

new_words = db_handler.fetch_new_words(kindle_db, local_db)
print new_words
db_handler.insert_new_words(kindle_db, local_db)

words = word_handler.get_words(new_words)
print words
