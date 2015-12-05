import sqlite3


class DBHandler:
    def insert_into_local(self, local_db, word_info):
        insertions = 0
        (word_key, word, stem, lang, timestamp, usages) = word_info
        conn = sqlite3.connect(local_db)
        c = conn.cursor()
        if not c.execute(('SELECT * FROM WORDS WHERE id = "%s"') % word_key).fetchone():
            print 'Inserting word: %s into local table WORDS' % word
            q1 = ('INSERT INTO WORDS VALUES("%s", "%s", "%s", "%s", "%s")') % (word_key, word, stem, lang, timestamp)
            c.execute(q1)
            conn.commit()
            for (word_key, usage, book_key, timestamp) in usages:
                print 'Inserting usages: %s into local table LOOKUPS' % usages
                q2 = ('INSERT INTO LOOKUPS VALUES("%s", "%s", "%s", "%s")') % (word_key, usage, book_key, timestamp)
                c.execute(q2)
                conn.commit()
        conn.close()

    def fetch_all(self, db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        query =  '''SELECT id, word, stem, lang, timestamp FROM WORDS'''
        words = c.execute(query).fetchall()
        lookups = dict()
        # Fetch a list of a words usages
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
        return [x for x in kindle_words if x not in local_words]

    def insert_new_words(self, kindle_db, local_db):
        new_words = self.fetch_new_words(kindle_db, local_db)
        map(lambda x: self.insert_into_local(local_db, x), new_words)

    def insert_translations(self, kindle_db, local_db):
        new_words = self.fetch_new(kindle_db, local_db)
        pass
        # translations = 
