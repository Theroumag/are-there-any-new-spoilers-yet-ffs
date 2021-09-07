#!/usr/bin/python#!/usr/bin/python

import requests
import json

sets = ["mid", "mic"] # sets to get updates for

for _set in sets: # set is a keyword so _set
    cache_file = "/root/.cache/" + _set + ".txt"
    open(cache_file, 'a').close() # create cache files if they dont exist

    with open(cache_file) as f:   saved_set = f.readlines() # read cache before overwritten

    url = "https://api.scryfall.com/cards/search?order=set&q=e:" + _set + "&unique=prints"
    r = requests.get(url)
    j = json.loads(r.text) # json for cards in set
    card_names = []

    for card in j['data']:
        card_names.append(card['name'])

    while j['has_more'] == True: # scryfall's API is pretty gay and paginates the set info json, instead of giving the whole set sanely
        next_page = j['next_page']
        r = requests.get(next_page)
        j = json.loads(r.text)
        for card in j['data']:
            card_names.append(card['name'])

    with open(cache_file, "w") as f: # write list to cache file
        f.writelines("\n".join(card_names))

    with open(cache_file) as f:   updated_set = f.readlines() # read freshly saved cache


    new_cards = set(saved_set).difference(updated_set) # compare old cache and new one

    print(f"Set: {_set.upper()}")
    print(new_cards)

# Written on Linux, if youre on windows change where the cache files are
