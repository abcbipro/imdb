import json
import httplib, urllib, base64
from pprint import pprint 
import time

key = 'f6d45a6aaeac45c2b9a61be284a4fa5d'

def save_json_file(result, out_file_name):
    try:
        f = open(out_file_name, 'w')
        writeable_str = json.dumps(result)
        f.write(writeable_str)
        f.close()
    except Exception as e:
        print 'Error at save_json_file!!!'
        print "[Errno {0}] {1}".format(e.errno, e.strerror)

def parse_response(data, name, i):
    person = {}
    person['id'] = i 
    person['name'] = name
    images = []
    data = json.loads(data)
    for value in data['value']:
        _d = {}
        _d['thumbnailUrl'] = value['thumbnailUrl']
        _d['contentUrl'] = value['contentUrl']
        images.append(_d)
    person['images'] = images
    return person

def search_image(name_list):
    result = []
    i = 0
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': key,
    }
    for name in name_list:
        i += 1
        print 'Geting person number', i, 'Name', name
        params = urllib.urlencode({
            # Request parameters
            'q': name,
            'count': '35',
        })
        try:
            conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
            conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            person = parse_response(data, name, i)
            result.append(person)
            print 'No.',i,'OK!!!', len(result)
            conn.close()
        except Exception as e:
            pprint(e)
        time.sleep(15)
    return result

def from_name_to_image(file_name):
    print 'Reading file name...'
    f = open(file_name, 'r')
    name_list = []
    for line in f: 
        name_list.append(line)
    print 'Searching for images...'
    json_persons = search_image(name_list)
    save_json_file(json_persons, "idol.json")
    print 'Done!'

if __name__ == "__main__":
    from_name_to_image("people_name.txt")