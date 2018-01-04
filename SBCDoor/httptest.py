import http.client
import json

connection = http.client.HTTPConnection('localhost',5000)

headers = {'Content-type': 'application/json'}

data = {
	"TAG": "pbkdf2:sha256:50000$pHiCKqph$8fb6e57e668259ea34213b21bd926e5da89",
	"ID_Sala": "2"
    }
    
json_data = json.dumps(data)

connection.request('POST', '/tryAccess', json_data, headers)

response = connection.getresponse()
print(response.read().decode())