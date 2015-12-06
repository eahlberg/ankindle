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

# new_words = db_handler.fetch_new_words(kindle_db, local_db)
# print new_words
# db_handler.insert_new_words(kindle_db, local_db)

# words = word_handler.get_words(new_words)
# print words

def update():
    word_info = db_handler.fetch_and_insert_new_words(kindle_db, local_db)
    word_keys = word_handler.get_word_keys(word_info)
    words = word_handler.get_words(word_info)
    translations = translation_handler.translate(words)
    if translations:
        translated_words = zip(word_keys, translations)
        db_handler.insert_translations(local_db, translated_words)


update()



# words = ["Enact"]
# print translation_handler.translate(words)
# word_info = db_handler.fetch_all(local_db)
# words = word_handler.get_words(word_info)
# word_keys = word_handler.get_word_keys(word_info)
# translation = translation_handler.translate(words)
# translated_words = zip(word_keys, translation)
# print translated_words

# db_handler.insert_translations(local_db, translated_words)
