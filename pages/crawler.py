class BoursoramaCrawler:
    """Crawler which allows you to generate the different pages."""
    
    def __init__(self, number_of_pages=10):
        self.url = "https://www.boursorama.com/actualite-economique/"
        self.number_of_pages = number_of_pages
        
    def run(self):
        "Generator that returns the pages to be scraped."
        for i in range(1, self.number_of_pages+1):
            yield f"{self.url}page-{str(i)}"