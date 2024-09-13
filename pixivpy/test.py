from pixivpy3 import *
import csv
import json
import sys
import time

token_file = 'token'
names_file = 'output/names.csv'
out_dir = 'output/jsons'
completed = 'output/completed.csv'

token = None

with open(token_file, 'r') as f:
    token = f.read().strip()

api = AppPixivAPI()
api.auth(refresh_token=token)

start_time = time.time()

with open(names_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        _id = row[0]
        name = row[1]
        jsons = []
        res = api.search_illust(
            name,
            search_target='exact_match_for_tags',
            sort='date_desc'
        )
        tot = len(res.illusts)
        jsons.extend(res.illusts)
        while res.next_url:
            next_qs = api.parse_qs(res.next_url)
            res = api.search_illust(**next_qs)
            if not res.illusts:
                break
            jsons.extend(res.illusts)
            tot += len(res.illusts)
        
        with open(f'{out_dir}/{_id}.json', 'w') as out:
            out.write(json.dumps(jsons))
        print(f'wrote {tot} entries for {_id}: {name} in {time.time() - start_time:.2f} seconds')
        with open(completed, 'a') as out:
            out.write(f'{_id},{name},{tot}\n')
        time.sleep(60)
        
