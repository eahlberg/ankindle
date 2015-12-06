import requests

class TranslationHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_url(self, words):
        base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='
        lang_string = 'en-sv'
        url = base_url + self.api_key + '&'
        return url + 'text=' + '&text='.join(words) + '&lang=' + lang_string

    def translate(self, words):
        if words:
            print '''[TranslationHandler] sending translation request with wordlist of length: %s''' % str(len(words))
            url = self.create_url(words)
            r = requests.get(url)
            # TODO: how to receive a list of alternative translations?
            translations = r.json()['text']
            return translations
