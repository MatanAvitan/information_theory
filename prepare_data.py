import requests
from pathlib import Path

BASE = Path('.')
DATA_PATH = BASE / 'data'
WRITING_PATH = DATA_PATH / 'sample.txt'
SAMPLE_URL  = 'https://raw.githubusercontent.com/kzjeef/algs4/master/burrows-wheelers/testfile/dickens.txt'

# Ensure the directory exists
DATA_PATH.mkdir(exist_ok=True)

# Download the file from the URL
response = requests.get(SAMPLE_URL)
response.raise_for_status()  # Raise an exception for HTTP errors

with open(WRITING_PATH, 'wb') as file:
        file.write(response.content)

