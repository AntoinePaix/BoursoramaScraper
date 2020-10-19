# BoursoramaScraper


BoursoramaScraper is a scraper that allows you to download relevant information from an article published on boursorama.

## Author

https://github.com/AntoinePaix

## Setup

You need **Python version >= 3.8**

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
from parser.video import VideoParser

article_links = BoursoramaCrawler(number_of_pages=10, video_links=True).run()

for article in article_links:

    if article.category == "video":
        print(VideoParser(article.url))  # printing
        VideoParser(article.url).save_to_csv()  # saving

    elif article.category == "article":
        print(ArticleParser(article.url).download_all())  # printing & saving all

    else:
        print(f"[-] Unknown article format : {article.url}")
        pass
```

To download images only of the first 100 pages :

```python
#app.py

from pages.crawler import BoursoramaCrawler
from parser.article import ArticleParser

article_links = BoursoramaCrawler(number_of_pages=100, video_links=False).run()

for article_link in article_links:
    ArticleParser(article_link.url).download_images()
```

To parse an article :

```python
# app.py

from parser.article import ArticleParser

url = "https://www.boursorama.com/actualite-economique/actualites/le-nobel-de-chimie-a-deux-chirurgiennes-des-genes-dont-une-francaise-4ee7deb2cefb65ec0fb9503542bb2047"

parser = ArticleParser(url)

print(parser)  # print some infos
parser.download_images()  # download images
```

To parse a video article :

```python
from parser.video import VideoParser

url = "https://www.boursorama.com/videos/actualites/ce-t-rex-vendu-31-8-millions-de-dollars-est-le-plus-cher-du-monde-e97c6d900ce264de872a6d32845dd112"

parser = VideoParser(url)

print(parser)
parser.save_to_csv()
```


**Very useful**, to consult the documentation for the ArticleParser class :

```python
# app.py

from parser.article import ArticleParser

help(ArticleParser)
```