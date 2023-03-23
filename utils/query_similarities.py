import csv
import json
import requests

IMAGES_TO_QUERY = '../data/source_data/Liste_automatisch_herauszufilternder_Bilder.csv'

QDRANT_QUERY_URL = 'http://localhost:6333/collections/onit/points'

N = 50

all_neighbours = []

def query_one_image(id):
  print(f'Querying: {id}')

  # qdrant query: search image by ID + get embedding vector
  query = {
    'filter': {
      'must': [
        { 'key': 'id', 'match': { 'value': id } },
      ],
    },
    'with_vector': True
  }

  response = requests.post(f'{QDRANT_QUERY_URL}/scroll', json=query)
  
  if response.status_code == 200:
    record = response.json()['result']['points'][0]

    # qdrant query: find N nearest neighbours to the record vector
    query = {
      'vector': record['vector'],
      'limit': N + 1, # Response *may* include the item itself
      'with_payload': True
    }
    
    response = requests.post(f'{QDRANT_QUERY_URL}/search', json=query)

    if response.status_code == 200:
      neighbours = response.json()['result']

      all_neighbours.append({
        'reference': record['payload'],
        'neighbours': [r['payload'] | { 'score': r['score'] } for r in neighbours if r['payload']['id'] != record['payload']['id']] 
      })

    else: 
      print('Error fetching neighbours')

  else:
    print('Error fetching record')

  
"""
Script starts here: query all files in the list...
"""
with open(IMAGES_TO_QUERY, 'r') as file:
  reader = csv.reader(file)

  for row in reader:
    # Rows: barcode, id, label, iiif, filename
    filename = row[0]

    identifier = filename[filename.rfind('/') + 1 : filename.rfind('.jpg')]
    
    query_one_image(identifier)

"""
...and write results to JSON file
"""
with open('../data/neighbours/neighbours.json', 'w') as file:
  json.dump(all_neighbours, file, indent=2)

    