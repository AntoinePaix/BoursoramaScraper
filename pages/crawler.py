from collections import namedtuple

from pages.all_article_links import AllArticleLinks


class BoursoramaCrawler:
    """Crawler which allows you to generate the different pages."""
    
    def __init__(self, number_of_pages=10, video_links=False):
        self.url = "https://www.boursorama.com/actualite-economique/"
        self.number_of_pages = number_of_pages
        self.video_links = video_links
        self.Link = namedtuple("Link", ["category", "url"])
        
    def generate_url(self):
        "Generator that returns the pages to be scraped."
        for i in range(1, self.number_of_pages+1):
            yield f"{self.url}page-{str(i)}"
            
    
    def category(self, link):
        if link.startswith("https://www.boursorama.com/videos"):
            return "video"
        else:
            return "article"
            
    def run(self):
        page_links = self.generate_url()
        for page in page_links:
            
            if not self.video_links:
                article_links = AllArticleLinks(page).extract_links(self.video_links)
            else:
                article_links = AllArticleLinks(page).extract_links(self.video_links)
                
            for article_link in article_links:
                yield self.Link(self.category(article_link), article_link)