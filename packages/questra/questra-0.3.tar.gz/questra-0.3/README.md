Questra — an alternative to the googlesearch-python library! Questra provides a simple and efficient interface for performing search queries, image searches, and translations through Google.

## What is Questra?

Questra is a library that allows you to integrate the powerful search capabilities of Google into your Python projects. It is designed to provide an intuitive and extendable tool that gives you flexible control over search queries, images, and translations. Questra simplifies interaction with Google, bypassing the need for bulky APIs.

## Key Features:

- **Search Queries:** Perform standard text search queries via Google.
- **Image Search:** Easily find images that match your queries.
- **Translations:** Use Google Translate to translate text between different languages.
- **Safe Mode:** Enable or disable safe search at your discretion.


### Installation:
```bash
pip install questra
```

### Usage Example:
```python
from questra import Client

client = Client()
results = client.search("Python programming", type='search', pages=2)
print(results)
```

### Search images and translate text:
```python
from questra import Client

client = Client()
results = client.search("Python programming", type='image', pages=2)
print(results)

print(client.translate("Hello", 'ru'))
```