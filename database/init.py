import json
import requests

QDRANT_URL = 'http://localhost:6333/collections/onit'

schema = {
  'name': 'onit',
  'vectors': {
    'size': 256,
    'distance': 'Cosine'
  }
}

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

# Delete existing index first
print('Deleting database...')
requests.delete(QDRANT_URL)

# Create the index
print('Creating new index')
response = requests.put(QDRANT_URL, data=json.dumps(schema), headers=headers)

if response.status_code != 200:
    print(f"Error creating schema: {response.text}")
else:
    print("Schema created successfully!")

# Make ID an indexed payload field
response = requests.post(QDRANT_URL + '/index', headers=headers, data=json.dumps({
  'field_name': 'id', 
  'field_schema': 'keyword'
}))

print('Done. Go to ' + QDRANT_URL)
