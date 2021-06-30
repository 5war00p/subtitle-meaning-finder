# requests module used for web requests
import requests

LANG_CODE = 'en_US'


def get_meaning(word):

    # params: a word (string)
    # return: meaning of the word (string)

    url = 'https://api.dictionaryapi.dev/api/v2/entries/' + LANG_CODE + '/' + word

    req = requests.get(url)
    res = req.json()

    try:
        meaning = res[0]['meanings'][0]['definitions'][0]['definition']
    except:
        meaning = None

    try:
        example = res[0]['meanings'][0]['definitions'][0]['example']
    except:
        example = None

    return meaning

# Test Drive Code

# print(get_meaning("tremble"))
