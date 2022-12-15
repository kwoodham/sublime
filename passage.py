#!/usr/bin/env python


# https://api.esv.org/docs/samples/

import sys
import requests


API_KEY = 'bf8dbb7a0fb39bd5bb138e3e5a0e261073252b80'
API_URL = 'https://api.esv.org/v3/passage/text/'


def get_esv_text(passage):
    params = {
        'q': passage,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': True
    }

    headers = {
        'Authorization': 'Token %s' % API_KEY
    }

    response = requests.get(API_URL, params=params, headers=headers)

    passages = response.json()['passages']

    return passages[0].strip() if passages else 'Error: Passage not found'


if __name__ == '__main__':
    passage = ' '.join(sys.argv[1:])

    if passage:
        print(get_esv_text(passage))
