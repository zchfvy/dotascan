import json
import os
import sys
from tqdm import tqdm

matches = []

local_dir = os.path.dirname(os.path.realpath(__file__))

fnames = os.listdir(sys.argv[1])
for fn in tqdm(fnames, desc="Loading Files"):
    if '.json' not in fn:
        continue
    fn = os.path.join(sys.argv[1], fn)
    with open(fn) as f:
        matches.append(json.load(f)['result'])

items = {}
with open(os.path.join(local_dir, 'items.json')) as f:
    items = json.load(f)['result']['items']

heroes = {}
with open(os.path.join(local_dir, 'heroes.json')) as f:
    heroes = json.load(f)['result']['heroes']
