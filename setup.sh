#!/bin/bash
echo "Downloading NLTK and TextBlob corpora..."
python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
python -m textblob.download_corpora

