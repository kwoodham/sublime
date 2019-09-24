#!/usr/bin/env python3

import sys
import requests


API_KEY = '17fb106e1997a5f8a1b6b6fe62a15a2004ae531e'
API_URL = 'https://api.esv.org/v3/passage/text/'

def get_esv_text(passage):
    params = {
        'q': passage,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': True,
        'include-short-copyright': False,
        'include-passage-references': True
    }

    headers = {
        'Authorization': 'Token %s' % API_KEY
    }

    response = requests.get(API_URL, params=params, headers=headers)

    passages = response.json()['passages']

    passage = passages[0].strip()
    if params['include-verse-numbers']:
        passage = passage.replace('[','(')
        passage = passage.replace(']',')')
    return passage

    # return response.json()

if __name__ == '__main__':
    passage = ' '.join(sys.argv[1:])

    if passage:
        print(get_esv_text(passage))
