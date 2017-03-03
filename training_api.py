import json
import time
from pprint import pprint
import httplib, urllib, base64
from search_api_ms import save_json_file

key = 'e3374926d8444f2696a36a6516b376cf'
personGroupId = 'celebrity'

def write_log(log_string):
    f = open('log.txt', 'a')
    f.write(log_string)
    f.close()

def open_json(file_name):
    try:
        with open(file_name) as open_file:
            celebrity = json.load(open_file)
        return celebrity
    except IOError as e:
        pprint (e)
        return None

def submit_person_face(personId, faceUrl, celebrity_id):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key,
    }

    body = json.dumps({
        'url': faceUrl
    })

    params = urllib.urlencode({})

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/"+personGroupId+"/persons/"+personId+"/persistedFaces?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        if (response.status == 200):
            data = json.loads(data)
            write_log ("[Info] Get face"+data['persistedFaceId'])
        else:
            write_log ("[Error] Face api at person no.",celebrity_id)
        conn.close()
        return data['persistedFaceId']
    except Exception as e:
        write_log ("lalaland error")
        return None

def create_person(celebritys):
    write_log("Start time: "+time.strftime("%a, %d %b %Y %H:%M:%S"))
    return_person_id = []
    for celebrity in celebritys[37:301]:
        write_log("-----------------------------------------------------------------------")
        write_log("[Info] Getting person"+str(celebrity['id'])+celebrity['name'].strip())
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': key
        }

        body = json.dumps({
            "name": celebrity['name'].strip(), 
            "userData": celebrity['id']
        })

        params = urllib.urlencode({
        })

        try:
            conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/persongroups/"+personGroupId+"/persons?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            if (response.status == 200):
                data = json.loads(data)
                person = {}
                person['id'] = celebrity['id']
                person['name'] = celebrity['name'].strip()
                person['personId'] = data['personId']
                person['faceId'] = []
                for link in celebrity['images'][7:]:
                    person['faceId'].append(submit_person_face(person['personId'], link['contentUrl'], person['id']))
                    time.sleep(4)
                return_person_id.append(person)
                write_log("[Info] Done with person no."+str(celebrity['id']))
            else:
                write_log("[Error] Create person at with person no." + str(celebrity['id']))
            conn.close()
        except Exception as e:
            write_log("[Error] create_person")
            pprint(e)

    f.write("End time: "+time.strftime("%a, %d %b %Y %H:%M:%S"))
    f.close()
    save_json_file(return_person_id, "personId.json")


if __name__ == "__main__":
    celebritys = open_json('idol.json')
    create_person(celebritys)