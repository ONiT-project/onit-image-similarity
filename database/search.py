import json
import requests

QDRANT_URL = 'http://localhost:6333/collections/onit/points/scroll'

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

query = {
  'filter': {
    'must': [
      { 'key': 'title', 'match': { 'value': 'Z15957400X_00125_page125_01' } }
    ]
  },
  'with_vector': True
}

response = requests.post(QDRANT_URL, data=json.dumps(query), headers=headers)

if response.status_code != 200:
  print(f"Error searching for point: {response.text}")
else:
  result = response.json()
  print(result['result'])
