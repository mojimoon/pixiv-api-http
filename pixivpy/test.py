from pixivpy3 import *
import csv
import json
import sys

token_file = 'pixivpy/token'
names_file = 'output/names.csv'
out_dir = 'output/jsons'

token = None

with open(token_file, 'r') as f:
    token = f.read().strip()

api = AppPixivAPI()
api.auth(refresh_token=token)

with open(names_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        _id = row[0]
        name = row[1]
        json_result = api.search_illust(
            name,
            search_target='exact_match_for_tags',
            sort='date_desc'
        )
        with open(f'{out_dir}/{_id}.json', 'w') as out:
            out.write(json.dumps(json_result))
        print(f'Wrote {name} to {out_dir}/{_id}.json')
        sys.exit(0)

