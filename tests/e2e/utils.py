import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
path = BASE_DIR.joinpath('components/json/campaigns/base.json')

campaigns = json.load(open(path))


def return_campaign(index = 0):
    return campaigns[int(index)]

'''
r = []
for c in range(1, 11):
    for a in range(1, 11):
        r.append([f'client-id-{c}',  f'advertiser-id-{a}',  randint(1, 100)])


with open('r.json', 'w') as f:
    f.write(json.dumps(r, indent=4, ensure_ascii=False))
    '''