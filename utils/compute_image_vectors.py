import csv
import glob
import numpy as np
from pathlib import Path
from progress.bar import Bar
from PIL import Image
from img2vec_pytorch import Img2Vec
from sklearn.decomposition import PCA

# https://github.com/christiansafka/img2vec

# EfficientNet-B3 produces vectors with 1536 dimensions 
img2vec = Img2Vec(cuda=False, model='efficientnet_b3')

print('reading folder...')
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
print('writing results to file')

with open('results.csv', 'w') as outfile:
  writer = csv.writer(outfile)
  writer.writerows(vectors)

print('reducing dimensions')

pca = PCA(n_components=256, svd_solver='full')
vec_reduced = pca.fit_transform(np.array([ row[1:] for row in vectors ]))
vec_reduced = [ row.tolist() for row in vec_reduced ]

print('writing results to file')

for idx, vec in enumerate(vec_reduced):
  id = vectors[idx][0]
  vec_reduced[idx].insert(0, id)

with open('results_256.csv', 'w') as outfile:  
  writer = csv.writer(outfile)
  writer.writerows(vec_reduced)

print('done')