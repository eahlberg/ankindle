#!/usr/bin/env python2

import sqlite3
import csv

def build_csv(filename, db_path):
    word_ids = fetch_word_ids(db_path)
    write_to_file(filename, word_ids)

def write_to_file(filename, word_ids):
    f = open(filename, 'w')

    for word_id in word_ids:
        example = fetch_word_example(word_id)
        s = word_id[3:].capitalize() + ',"' + example + '"\n'
        f.write(s.encode('UTF-8'))

    f.close()

def fetch_words_in_csv(filename):
    words = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.append(row[0])
    return words

def fetch_words(db_path):
    return [word_id[3:].capitalize() for word_id in fetch_word_ids(db_path).keys()]

def fetch_word_ids(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    word_ids = {word[0] : word[1:] for word in c.execute('SELECT * FROM WORDS')}
    conn.close()
    return word_ids

def fetch_word_example(word_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = "SELECT * FROM LOOKUPS WHERE word_key = '" + word_id + "'"
    result = c.execute(query).fetchone()
    example = result[5]
    conn.close()
    return example

def fetch_new_words(db_path, filename):
    words = fetch_words(db_path)
    words_in_csv = fetch_words_in_csv(filename)
    return list(set(words) - set(words_in_csv))


def create_url(words):
    base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='
    api_key = 'HIDDEN'
    lang_string = 'en-sv'
    url = base_url + api_key + '&'
    return '"' + url + 'text=' + '&text='.join(words) + '&lang=' + lang_string + '"'

db_path = '/Volumes/Kindle/system/vocabulary/vocab.db'
# db_path = 'vocab.db'
csvfile = 'words.csv'
# build_csv(csvfile, db_path)
# words = fetch_words_in_csv(csvfile)
new_words = fetch_new_words(db_path, csvfile)
print create_url(new_words)
# print words
