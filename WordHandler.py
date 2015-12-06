

class WordHandler:
    def get_words(self, word_info):
        return map(lambda x: x[1].capitalize(), word_info)

    def get_word_keys(self, word_info):
        return map(lambda x: x[0], word_info)
