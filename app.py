from pages.crawler import BoursoramaCrawler
from parser.article import ArticleParser


if __name__ == "__main__":
    
    try:
            
        article_links = BoursoramaCrawler(number_of_pages=10, video_links=False).run()

        for article_link in article_links:
            print(article_link)
            print(ArticleParser(article_link).download_all())
            print("-" * 50)
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt, stop scraping.")