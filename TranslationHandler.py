import requests

class TranslationHandler:
    def create_url(self, words):
        base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='
        # api_key = 'HIDDEN'
        lang_string = 'en-sv'
        url = base_url + api_key + '&'
        return url + 'text=' + '&text='.join(words) + '&lang=' + lang_string

    def translate(self, words):
        url = self.create_url(words)
        return requests.get(url).json()['text']
