import json
import requests
import uuid

QDRANT_URL = 'http://localhost:6333/collections/onit/points'

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

records = []

with open('../data/vectors/D17_256d.jsonl') as f:
  for line in f:
    # id, url, title, vec
    records.append(json.loads(line))

print('Loaded ' + str(len(records)) + ' records')

# Convert JSON objects to Qdrant's expected format
batch = []
for rec in records:
  batch.append({
    'id': str(uuid.uuid4()),
    'vector': rec['vec'],
    'payload': { 
      'id': rec['id'],
      'local_url': rec['local_url'],
      'iiif_url': rec['iiif_url']
    }
  })

print('Ingesting batch...')

response = requests.put(QDRANT_URL, data=json.dumps({ 'points': batch }), headers=headers)

if response.status_code != 200:
  print(f"Error indexing data: {response.text}")
else:
  print("Data indexed successfully!")

print('Done indexing ' + str(len(batch)) + ' records')