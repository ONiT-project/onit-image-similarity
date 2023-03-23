import json
import numpy as np
import os
from pathlib import Path
from progress.bar import Bar
from PIL import Image
from img2vec_pytorch import Img2Vec
from sklearn.decomposition import PCA
from iiif_correspondence import load_corresponence

# https://github.com/christiansafka/img2vec

# EfficientNet-B3 produces vectors with 1536 dimensions 
img2vec = Img2Vec(cuda=False, model='efficientnet_b3')

print('Reading folder...')

filenames = list(Path('../../onit-iiif-harvest/data/clipped/D17/').rglob('*.jpg'))

print(f'{len(filenames)} files')

vectors = []

bar = Bar('Processing', max=len(filenames))

for path in filenames:
  f = str(path.resolve())

  id = f[f.rfind('/') + 1 : f.rfind('.jpg')]

  try:
    img = Image.open(f)
    img = img.convert('RGB') # this sucks 

    vec = img2vec.get_vec(img)

    row = [ id ]
    row.extend(vec)

    vectors.append(row)
  except Exception as e:
    print('Error loading image: ' + f)
  
  bar.next()

bar.finish()

print('Reducing dimensions')

pca = PCA(n_components=256, svd_solver='full')
vec_reduced = pca.fit_transform(np.array([ row[1:] for row in vectors ]))
vec_reduced = [ row.tolist() for row in vec_reduced ]

print('Loading IIIF correspondence table')
iiif = load_corresponence()

records = []

for idx, vec in enumerate(vec_reduced):
  id = vectors[idx][0]

  barcode = id[:id.index('_')]

  records.append({
    'id': id,
    'local_url': 'http://localhost/images/' + barcode + '/' + id + '.jpg',
    'iiif_url': iiif[id + '.jpg'], 
    'vec': vec
  })

print('Writing results to file')

with open('results_256.jsonl', 'a') as outfile:  

  for record in records:
    outfile.write(json.dumps(record) + os.linesep)

print('done')
