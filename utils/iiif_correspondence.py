import csv

def load_corresponence():
  index = {}

  with open('../data/source_data/D17_IIIF.csv', 'r') as file:
    reader = csv.reader(file)

    for row in reader:
      filename = row[4]
      iiif_url = row[3]

      index[filename] = iiif_url

  return index
