import json
import os
import sys
from tqdm import tqdm

matches = []
items = {}
heroes = {}

local_dir = os.path.dirname(os.path.realpath(__file__))


def _load():
    global matches

    fnames = os.listdir(sys.argv[1])
    for fn in tqdm(fnames, desc="Loading Files"):
        if '.json' not in fn:
            continue
        fn = os.path.join(sys.argv[1], fn)
        with open(fn) as f:
            try:
                json_obj = json.load(f)
            except ValueError:
                print("Failed to load {}.".format(fn))
                continue
            if 'result' not in json_obj:
                print("Skipping {} due to bad data.".format(fn))
                continue
            matches.append(json_obj['result'])


def get_matches():
    global matches
    if not matches:
        _load()
    return matches


def get_items():
    global items
    if not items:
        with open(os.path.join(local_dir, 'items.json')) as f:
            items = json.load(f)['result']['items']
    return items


def get_heroes():
    global heroes
    if not heroes:
        with open(os.path.join(local_dir, 'heroes.json')) as f:
            heroes = json.load(f)['result']['heroes']
    return heroes
