# ONiT Image Similarity

Utilities for searching images by visual similarity, using off-the-shelf open source technology.

## Overview

In this repository, you will find:

- Python scripts for computing embedding vectors from folders of image files using [img2vec](https://github.com/christiansafka/img2vec).
- A Docker configuration for running the [Qdrant](https://qdrant.tech/) vector search engine locally
- Python scripts for ingesting the embedding vectors into qdrant and running nearest-neighbour searches on lists of images

Scripts were developed specifically for the [ONiT](https://onit.oeaw.ac.at/) research project, which means there are some
project-specific conventions and schemas baked into the scripts. Use at your own caution!

## Generating Image Embedding Vectors

The script [utils/compute_image_vectors.py](blob/main/utils/compute_image_vectors.py) performs the following steps:

- Starting from a configured folder path, it loads all `*.jpg` images from the folder and its subfolders. __Images are not included in this repository!__
- For each image, it generates an embedding vector (using `efficientnet_b3`).
- Converts vectors to 256 dimensions using PCA.
- Loads a CSV file with publicly accessible [IIIF](https://iiif.io/) links for each image. (Example file included in this repository [here](blob/main/data/source_data/D17_IIIF.csv))
- Generates a result file with the following data for each image. (The result file in in [JSONL](https://jsonlines.org/) format, and written to the `data/vectors` folder).
  - image identifier (= filename without `.jpg` extension)
  - IIIF image URL
  - embedding vector

## Bootstrapping Qdrant

To enable fast similarity search, image embedding vectors are loaded into a [Qdrant](https://qdrant.tech/) database. The `database` 
folder contains a `docker-compose.yml` file which starts an empty Qdrant instance on the default port (6333).

- Run `docker compose up` to start the database server.
- Run `python init.py` to initialize an empty database collection (named `onit`), with a schema matching our image embedding data.
- Run `python ingest.py` to import the JSONL data file (generated in the last step) to Qdrant.
- The `search_example.py` script shows how you can run a nearest neighbour search for a specific image, using its ID as a query parameter. Due
  to the way Qdrant works, this is a two-step query:
  - A first query is needed to retrieve the vector for an image, given its ID
  - Using the vector as an input, a second query retrieves a list of N nearby vectors (and image records)
  - Note that the second query __will include the original query image__ as well.

## Bulk Similarity Utility

The script [utils/query_similarities.py](blob/main/utils/query_similarities.py) takes a list of image IDs as input, and runs a bulk-search
for N (currently configured to 50) nearest neighbours in Qdrant. The output is written to a [JSON file](https://github.com/travelogues/onit-image-similarity/blob/main/data/neighbours/neighbours.json).

The JSON file contains an array of `reference` images, and their `neighbours`. The script includes the `score` for each neighbour, a number delivered by Qdrant as a measure of relative similarity.

### HTML Preview

The script [utils/generate_html_preview.py](blob/main/utils/generate_html_preview.py) takes the JSON similarity result as input, and generates an HTML preview file.
 

