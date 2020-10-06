from pages.all_article_links import AllArticleLinks
from pages.crawler import BoursoramaCrawler
from parser.article import ArticleParser


if __name__ == "__main__":
    
    try:
            
        crawler = BoursoramaCrawler(number_of_pages=10)
        page_links = crawler.run()  # Generates the urls of the first 10 news pages
        
        for link in page_links:
            article_links = AllArticleLinks(link).extract_links(video_links=False)
            for article_link in article_links:
                print(article_link)
                print(ArticleParser(article_link).download_all())
                print("-" * 50)
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt, stop scraping.")