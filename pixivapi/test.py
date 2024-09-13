from pixivapi import Client, Size
import csv
import json
import sys

token_file = 'token'
names_file = 'output/names.csv'
out_dir = 'output/json'

token = None

with open(token_file, 'r') as f:
    token = f.read().strip()

client = Client(language='Japanese')
client.authenticate(token)

with open(names_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        _id = row[0]
        name = row[1]
        json_result = client.search_illustrations(
            name,
            search_target='exact_match_for_tags',
        )
        with open(f'{out_dir}/{_id}.json', 'w') as out:
            out.write(json.dumps(json_result))
        print(f'Wrote {name} to {out_dir}/{_id}.json')
        sys.exit(0)
