#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Download NLTK/TextBlob corpora to the correct location
export NLTK_DATA="/opt/render/nltk_data"
mkdir -p $NLTK_DATA
python -m nltk.downloader punkt averaged_perceptron_tagger wordnet punkt_tab -d $NLTK_DATA
python -m textblob.download_corpora



