import os
import sys
import requests

api_url = 'http://127.0.0.1:1145/search'

out_file = 'output/search.json'

'''
SearchParam:
参数	类型	描述	默认值
word	string	搜索词	必填
type	SearchType	搜索类型	illust
template	TemplateType	预设模板	无
mode	SearchMode	搜索模式	tag
order	SearchOrder	排序方法	date
blt	number	最少收藏数	0
restrict	Restrict	限制等级	safe
start	number	起始索引	0
length	number	索引长度	60
lang	Lang	语言	配置文件
'''

post_data = {
    'word': '柚鳥ナツ',
    'type': 'artwork',
    'mode': 'full',
    'order': 'date',
    'restrict': 'all',
    'length': 25000,
}

response = requests.post(api_url, json=post_data)

if response.status_code == 200:
    with open(out_file, 'w') as f:
        f.write(response.text)
    print('Search test success, response saved to %s' % out_file)
else:
    print('Search test failed, status code: %d' % response.status_code)
    print(response.text)
    sys.exit(1)
