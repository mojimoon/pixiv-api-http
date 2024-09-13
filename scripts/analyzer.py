import json
import csv
from collections import defaultdict

'''
data sample
{"id":122392009,"title":"ゆず","cover":"http://127.0.0.1:1145/proxy/c/250x250_80_a2/img-master/img/2024/09/13/16/12/18/122392009_p0_square1200.jpg","tags":["メイド服","花岡ユズ(メイド)","ブルーアーカイブ","ブルアカ","花岡ユズ"],"createTime":1726211538000,"updateTime":1726211538000,"restrict":"safe","total":1,"author":{"name":"みっくすじゅーす","id":37878188}},
'''

srcs = [
    'output/json/029.json',
    'output/json/030.json',
    'output/json/031.json',
    'output/json/032.json',
]

names = 'output/names.csv'

output1 = 'result/tag_freq.csv'
output2 = 'result/name_comb.csv'
output3 = 'result/authors.csv'

def load_csv(src):
    with open(src, 'r') as f:
        return {row[0]: row[1] for row in csv.reader(f)}

def load_json(src):
    with open(src, 'r') as f:
        return json.load(f)

def analyze():
    names_dict = load_csv(names)
    names_set = set(names_dict.values())
    pid_set = set()
    tag_freq = {idx: defaultdict(int) for idx in range(29, 34)}
    author_freq = {idx: defaultdict(int) for idx in range(29, 34)}
    author_dict = defaultdict(str)
    name_comb = defaultdict(int)
    for idx, src in zip(range(29, 33), srcs):
        data = load_json(src)
        for illust in data['results']:
            tags = illust['tags']
            for tag in tags:
                tag_freq[idx][tag] += 1
            author_freq[idx][illust['author']['id']] += 1
                
            if illust['id'] in pid_set:
                continue

            pid_set.add(illust['id'])
            for tag in tags:
                tag_freq[33][tag] += 1
            author_freq[33][illust['author']['id']] += 1
            _names = names_set.intersection(tags)
            name_comb[tuple(_names)] += 1

            if not author_dict[illust['author']['id']]:
                author_dict[illust['author']['id']] = illust['author']['name']
    with open(output1, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['tag', 'yuzu', 'momoi', 'midori', 'aris', 'total', 'ratio'])
        all_tags = set()
        for idx in range(29, 34):
            all_tags.update(tag_freq[idx].keys())
        tags = list(all_tags)
        tags.sort(key=lambda x: tag_freq[33][x], reverse=True)
        for tag in tags:
            if tag_freq[33][tag] < 10:
                continue
            writer.writerow([tag, 
                *[tag_freq[idx][tag] for idx in range(29, 34)],
                sum(tag_freq[idx][tag] for idx in range(29, 33)) / tag_freq[33][tag]
            ])
    with open(output2, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['names', 'count'])
        name_combs = list(name_comb.keys())
        name_combs.sort(key=lambda x: name_comb[x], reverse=True)
        for _names in name_combs:
            writer.writerow(['_'.join(_names), name_comb[_names]])
    with open(output3, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'author', 'yuzu', 'momoi', 'midori', 'aris', 'total', 'ratio'])
        all_authors = set()
        for idx in range(29, 34):
            all_authors.update(author_freq[idx].keys())
        authors = list(all_authors)
        authors.sort(key=lambda x: author_freq[33][x], reverse=True)
        for author in authors:
            if author_freq[33][author] < 10:
                continue
            writer.writerow([author, author_dict[author].replace(',', ' '),
                *[author_freq[idx][author] for idx in range(29, 34)],
                sum(author_freq[idx][author] for idx in range(29, 33)) / author_freq[33][author]
            ])

if __name__ == '__main__':
    analyze()