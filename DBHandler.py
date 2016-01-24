import sqlite3
from Word import *

class DBHandler:
    def init(self, local_db):
        conn = sqlite3.connect(local_db)
        c = conn.cursor()
        q1 = '''CREATE TABLE WORDS (INTEGER PRIMARY KEY, id TEXT, word TEXT,
        stem TEXT, lang TEXT, timestamp INTEGER DEFAULT 0);'''
        q2 = '''CREATE TABLE LOOKUPS (INTEGER PRIMARY KEY, word_key TEXT, usage
        TEXT, book_key TEXT, timestamp INTEGER DEFAULT 0);'''
        q3 = '''CREATE TABLE TRANSLATIONS (INTEGER PRIMARY KEY, word_key TEXT,
        translation TEXT);'''
        c.execute(q1)
        c.execute(q2)
        c.execute(q3)
        conn.commit()
        conn.close()

    def insert_into_local(self, local_db, word_info):
        insertions = 0
        (word_key, word, stem, lang, timestamp, usages) = word_info
        conn = sqlite3.connect(local_db)
        c = conn.cursor()
        if not c.execute(('SELECT * FROM WORDS WHERE id = "%s"') % word_key).fetchone():
            print '[DBHandler] Inserting word: %s into local table WORDS' % word
            q1 = ('INSERT INTO WORDS (id, word, stem, lang, timestamp) VALUES("%s", "%s", "%s", "%s", "%s")') % (word_key, word, stem, lang, timestamp)
            c.execute(q1)
            for (word_key, usage, book_key, timestamp) in usages:
                q2 = ('''INSERT INTO LOOKUPS (word_key, usage, book_key,
                      timestamp) VALUES("%s", "%s", "%s", "%s")''') % (word_key, usage, book_key, timestamp)
                c.execute(q2)
            conn.commit()
        conn.close()

    def fetch_all(self, db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        query =  '''SELECT id, word, stem, lang, timestamp FROM WORDS'''
        words = c.execute(query).fetchall()
        lookups = dict()
        # Fetch a list of a word usages
        for (word_key, _, _, _, _) in words:
            lookup_query = 'SELECT word_key, usage, book_key, timestamp FROM LOOKUPS WHERE word_key = "%s"' % word_key
            usages = c.execute(lookup_query).fetchall()
            lookups[word_key] = usages
        conn.close()
        return [(word_key, word, stem, lang, timestamp, lookups[word_key]) for
                (word_key, word, stem, lang, timestamp) in words]

    def fetch_new_words(self, kindle_db, local_db):
        kindle_words = self.fetch_all(kindle_db)
        local_words = self.fetch_all(local_db)
        local_word_keys = map(lambda word: word[0], local_words)

        return [x for x in kindle_words if x[0] not in local_word_keys]

    def fetch_and_insert_new_words(self, kindle_db, local_db):
        new_words = self.fetch_new_words(kindle_db, local_db)
        map(lambda x: self.insert_into_local(local_db, x), new_words)
        return new_words

    def fetch_all_with_translations(self, local_db):
        word_infos = self.fetch_all(local_db)
        conn = sqlite3.connect(local_db)
        c = conn.cursor()

        words = []
        for (word_key, word, stem, lang, timestamp, lookups) in word_infos:
            query = ('SELECT translation FROM TRANSLATIONS WHERE word_key = "%s"') % word_key
            translation = c.execute(query).fetchone()
# TODO: temp. fix: uses 0 to extract only the transl., not whole tuple
            lookups_str = map(lambda lookup: lookup[1], lookups)
            words.append(Word(word_key, word, stem, lang, timestamp, lookups_str,
                              translation[0]))
        conn.close()
        return words

    def insert_translation(self, local_db, word_key, translation):
        conn = sqlite3.connect(local_db)
        c = conn.cursor()
        # TODO: make this check a function
        if not c.execute(('SELECT * FROM TRANSLATIONS WHERE word_key = "%s"') % word_key).fetchone():
            print ('[DBHandler] Inserting %s with translation %s into local table TRANSLATIONS') % (word_key, translation)
            query = ('INSERT INTO TRANSLATIONS (word_key, translation) VALUES("%s", "%s")') % (word_key, translation)
            c.execute(query)
            conn.commit()
        conn.close()

    def insert_translations(self, local_db, words):
        map(lambda (word_key, translation): self.insert_translation(local_db, word_key,
                                                 translation), words)
