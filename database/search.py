import json
import requests

QDRANT_URL = 'http://localhost:6333/collections/onit/points'

K = 20

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

def search_nearest_neighbours(id, k=K):
  query = {
    'filter': {
      'must': [
        { 'key': 'title', 'match': { 'value': id } }
      ]
    },
    'with_vector': True
  }

  response = requests.post(QDRANT_URL + '/scroll', data=json.dumps(query), headers=headers)

  if response.status_code != 200:
    print(f'Record not found: {id}')
  else:
    top_result = response.json()['result']['points'][0]

    response = requests.post(QDRANT_URL + '/search', headers=headers, data=json.dumps({
      'vector': top_result['vector'],
      'limit': k + 1, # Response *may* include the item itself, which we'll filter
      'with_payload': True
    }))

    if response.status_code != 200:
      print(f'Error: {response.text}')
    else:
      return response.json()['result']
    

"""
Run sample search
"""

neighbours = search_nearest_neighbours('Z15957400X_00125_page125_01')
print(neighbours)

