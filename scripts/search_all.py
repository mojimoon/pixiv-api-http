import os
import sys
import requests
import time
import csv

api_url = 'http://127.0.0.1:1145/search'
sleep_time = 180

in_file = 'output/names.csv'
out_dir = 'output/json'
completed_ids = 'output/completed.csv'

post_data = {
    'type': 'artwork',
    'mode': 'full',
    'order': 'date',
    'restrict': 'all',
    'length': 25000,
}

completed = set()

if os.path.exists(completed_ids):
    with open(completed_ids, 'r') as f:
        for line in f:
            completed.add(int(line.split(',')[0]))

with open(in_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if int(row[0]) in completed:
            print('Skip %s' % row[1])
            continue
        post_data['word'] = row[1]
        response = requests.post(api_url, json=post_data)
        if response.status_code == 200:
            out_file = os.path.join(out_dir, row[0] + '.json')
            with open(out_file, 'w') as f:
                f.write(response.text)
            total = response.text.count('updateTime')
            print('Search test success, %d records found for %s, response saved to %s' % (total, row[1], out_file))
            if total == 0:
                print('No records found. Check if the name is correct.')
            else:
                with open(completed_ids, 'a') as f:
                    f.write('%d,%s,%d\n' % (int(row[0]), row[1], total))
        else:
            print('Search test failed, status code: %d' % response.status_code)
            print(response.text)
            sys.exit(1)
        time.sleep(sleep_time)