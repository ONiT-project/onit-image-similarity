import csv
import json
import os

records = []

with open('../data/D16_clipped_256d.csv', 'r') as infile:
  reader = csv.reader(infile)

  for row in reader:
    filename = row[0]

    vector = [ float(x) for x in row[1:] ]

    barcode = filename[:filename.index('_')]

    record = {
      'id': filename,
      'url': 'http://localhost/images/' + barcode + '/' + filename + '.jpg',
      'title': filename,
      'reproduction': 'http://localhost/images/' + barcode + '/' + filename + '.jpg',
      'vec': vector
    }

    records.append(record)

with open('results.jsonl', 'a') as outfile:

  for record in records:
    outfile.write(json.dumps(record) + os.linesep)

print('Done')



