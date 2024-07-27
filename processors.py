import deepl
import requests
from utils import meaning_to_string, contain_foreign

# https://dictionaryapi.dev/
dictionary_url_base = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

class Result:
    def __init__(self, text):
        self.text = text

def translate_word(from_word):
    response = requests.get(dictionary_url_base + from_word)
    if response.status_code == 200:
        resJson = response.json()
        def parseWord(word): return "\n\n".join(
            map(meaning_to_string, word['meanings']))
        return Result("\n\n".join(map(parseWord, resJson)))
    elif "message" in response.json():
        return Result(response.json()['message'])
    else:
        return Result("Network Error")


def translate_sentences(from_text, auth_key, target_lang):
    from_text = from_text.replace("\r\n", " ")
    from_text = from_text.replace("\n\r", " ")
    from_text = from_text.replace("\n", " ")

    translator = deepl.Translator(auth_key)

    if contain_foreign(from_text):
        result = translator.translate_text(from_text, target_lang="EN-US")
    else:
        result = translator.translate_text(
            from_text, target_lang=target_lang)

    return Result(result.text)