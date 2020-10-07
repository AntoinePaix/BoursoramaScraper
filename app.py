from pages.crawler import BoursoramaCrawler
from parser.article import ArticleParser
from parser.video import VideoParser


if __name__ == "__main__":
    
    try:
            
        article_links = BoursoramaCrawler(number_of_pages=2, video_links=True).run()

        for article in article_links:
            if article.category == "video":
                print(VideoParser(article.url))
                VideoParser(article.url).save_to_csv()
            elif article.category == "article":
                print(ArticleParser(article.url).download_all())
            else:
                print("Unknown article format.")
                pass
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt, stop scraping.")