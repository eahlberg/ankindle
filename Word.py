class Word:
    def __init__(self, word_key, word, stem, lang, timestamp, usages, translation):
        self.word_key = word_key
        self.word = word
        self.stem = stem
        self.lang = lang
        self.timestamp = timestamp
        self.usages = usages
        self.translation = translation

    def __repr__(self):
        return '%s, %s, %s, %s, %s, %s, %s' % (self.word_key, self.word,
                                               self.stem, self.lang,
                                               self.timestamp, self.usages,
                                               self.translation)

    def to_csv(self):
        return ('%s\t%s - %s\n' % (self.word.capitalize(), self.translation,
                                     '/'.join(self.usages))).encode('utf-8')
