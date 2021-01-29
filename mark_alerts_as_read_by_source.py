import json
import requests
import subprocess

data = '{ "query": { "bool": { "must": { "query_string": { "query": "(source:\\"MY-MISP\\")" } }, "filter": { "term": { "status": "New"} } } }, "stored_fields": "id", "size" : 10000 }'
response = requests.post('http://ELASTIC_URL:9200/the_hive_15/_search', data=data, headers={'Content-Type': 'application/json'})
df = response.json()

for i in range(100):
    df_small = df['hits']['hits'][i*100:(i+1)*100]
    list_id = '","'.join([x['_id'] for x in df_small if x['_type'] == 'doc'])
    data = '{"ids": ["' + list_id + '"], "status": "Ignored" }'
    cmd = """/usr/bin/curl -XPATCH -H 'Content-Type: application/json' -H 'Authorization: Bearer h3jkh34432hj342jkh3jk24h234kj' 'http://THE_HIVE_URL:9000/api/alert/_bulk' -d '{"ids": [ "%s" ], "status": "Ignored"}'""" % (list_id)
    subprocess.call(cmd, shell=True)
