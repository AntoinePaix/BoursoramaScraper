# BoursoramaScraper


BoursoramaScraper is a scraper that allows you to download relevant information from an article published on boursorama.

## Author

https://github.com/AntoinePaix

## Setup

You need **Python version >= 3.6**

```
git clone https://github.com/AntoinePaix/BoursoramaScraper.git

cd BoursoramaScraper

pip install -r requirements.txt
```

# How to use

```
python app.py
```

To download the content of the first 10 pages :

```python
#app.py

from pages.crawler import BoursoramaCrawler
from parser.article import ArticleParser

article_links = BoursoramaCrawler(number_of_pages=10, video_links=False).run()

for article_link in article_links:
    print(article_link)
    print(ArticleParser(article_link).download_all())
    print("-" * 50)
```

To download images only of the first 100 pages :

```python
#app.py

from pages.crawler import BoursoramaCrawler
from parser.article import ArticleParser

article_links = BoursoramaCrawler(number_of_pages=100, video_links=False).run()

for article_link in article_links:
    ArticleParser(article_link).download_images()
```

To parse an article :

```python
# app.py

from parser.article import ArticleParser

url = "https://www.boursorama.com/actualite-economique/actualites/trump-minimise-la-menace-du-covid-19-et-l-hypothese-de-la-defaite-6759a52dc9f34afa7f065c0a0c5e689d"

parser = ArticleParser(url)

print(parser.title)  # print title
print(parser.url)  # print url
parser.download_images()  # download images
```

**Very useful**, to consult the documentation for the ArticleParser class :

```python
# app.py

from parser.article import ArticleParser

help(ArticleParser)
```