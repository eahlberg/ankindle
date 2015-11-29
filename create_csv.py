#!/usr/bin/env python2

import sqlite3


def fetch(db_path):
    create_csv(db_path)


def create_csv(db_path):
    f = open('words.csv', 'w')

    word_keys = fetch_word_keys(db_path)
    for word_key in word_keys:
        example = fetch_word_example(word_key)
        s = word_key[3:].capitalize() + ',"' + example + '"\n'
        f.write(s.encode('UTF-8'))

    f.close()

def fetch_words(db_path):
    return [word_key[3:].capitalize() for word_key in fetch_word_keys(db_path).keys()]

def fetch_word_keys(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    word_keys = {word[0] : word[1:] for word in c.execute('SELECT * FROM WORDS')}
    conn.close()
    return word_keys

def fetch_word_example(word_key):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = "SELECT * FROM LOOKUPS WHERE word_key = '" + word_key + "'"
    result = c.execute(query).fetchone()
    example = result[5]
    conn.close()
    return example

def create_url(words):
    base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='
    api_key = 'HIDDEN'
    lang_string = 'en-sv'
    url = base_url + api_key + '&'
    return '"' + url + 'text=' + '&text='.join(words) + '&lang=' + lang_string + '"'

# print create_url(['hello', 'moose', 'cat'])
db_path = '/Volumes/Kindle/system/vocabulary/vocab.db'
# db_path = 'vocab.db'
create_csv(db_path)
# wk = fetch_word_keys(db_path)
# words = fetch_words(db_path)
# print create_url(words)
# print wk.keys()
# fetch(db_path)
