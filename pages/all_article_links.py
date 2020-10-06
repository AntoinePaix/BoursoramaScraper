import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from locators.article_links import ArticleLinksLocators

class AllArticleLinks:
    def __init__(self, url):
        self.url = url

    @property
    def soup(self):
        "Returns beautifulsoup object."
        content = requests.get(self.url).content
        return BeautifulSoup(content, "html.parser")

    @property
    def title(self):
        "Returns the title of the page."
        return self.soup.title.text.strip()
    
    def extract_links(self, video_links=False):
        """
        Extract all article links from a page.
        `video_links = False` (default) : returns all article links without video links.
        `video_links = True` : returns all links (video links included).
        """
        boursorama_base_url = "https://www.boursorama.com"
        articles_body = self.soup.select_one(ArticleLinksLocators.BODY_LINKS)
        
        all_links = [urljoin(boursorama_base_url, bloc.select_one(ArticleLinksLocators.HREF_LINK)['href']) for bloc in articles_body.select(ArticleLinksLocators.INDIVIDUAL_BLOC)]

        links_without_videos = [link for link in all_links if link.startswith("https://www.boursorama.com/actualite-economique/actualites/")]
        
        if not video_links:
            return links_without_videos
        
        return all_links
    