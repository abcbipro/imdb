import json
from pprint import pprint 

# with data as data_file:
#data = data.encode('utf-8') 
with open('idol.json') as open_file:
	tmp = json.load(open_file)

for p in tmp[4]['images']:
	print json.dumps({
        'url': p['contentUrl']
    })
	print p['contentUrl']

# for picture in data["value"]:
# 	pprint (picture["name"])


# import io, json
# with io.open('data.txt', 'w', encoding='utf-8') as f:
#   	f.write(unicode(json.dumps(data, ensure_ascii=False)))
