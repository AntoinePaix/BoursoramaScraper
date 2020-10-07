import os
import csv
import datetime

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

from locators.article import ArticleLocators

class ArticleParser:
    """Main class that parses, extracts and saves relevant information from different articles"""
    
    def __init__(self, article_url):
        self.url = article_url
        self.images_folder = "Images"
        self.datas_csv = "datas.csv"
    
    def html_content(self):
        "Returns HTML content."
        return requests.get(self.url).content
    
    @property
    def soup(self):
        "Returns beautifulsoup object for parsing."
        return BeautifulSoup(self.html_content(), "html.parser")
    
    @property
    def _id(self):
        "Returns the id of the article."
        return self.url.split('-')[-1]
    
    @property    
    def title(self):
        "Returns the title of the article."
        return self.soup.title.text[:-13]
    
    @property
    def author(self):
        "Returns the author of the article (most of the time the news agency)."
        return self.soup.select_one(ArticleLocators.AUTHOR).text.strip()
    
    def __repr__(self):
        return f'<Article(url="{self.url}" title="{self.title}" author="{self.author}" date="{self.date()}" id="{self._id}" images={len(self.images())})'
    
    def date(self, timestamp=False):
        "Returns the publication date of the article."
        date = self.soup.select_one(ArticleLocators.DATE).text.strip()
        date_object = datetime.datetime.strptime(date, "%d/%m/%Y à %H:%M")
        
        if not timestamp:
            return date_object.strftime("%d/%m/%Y %H:%M")
        else:
            return int(date_object.timestamp())
        
    @property
    def article_body(self):
        "Returns the content of the article."
        
        return self.soup.select_one(ArticleLocators.ARTICLE_BODY).text.strip()
    
    @property
    def redactors(self):
        """Returns the editors of the article.
        Warning, sometimes the name of the editor is not mentioned in the article,
        in this case the `redactors` function returns the last paragraph of the article."""
        return self.soup.select_one(ArticleLocators.ARTICLE_BODY).select('p')[-1].text.strip()
    
    @property
    def number_of_comments(self):
        return self.soup.select_one(ArticleLocators.NUMBER_OF_COMMENTS).text.strip().split()[0]

    def images(self, link=True):
        """
        `link = True` (default) : returns a list of the links of the images.
        `link = False` : returns a list containing the names of the images.
        """
        
        if link:
            return [url[ArticleLocators.IMAGE_URL] for url in \
                self.soup.select(ArticleLocators.IMAGES_LIST)]
        else:
            return [url[ArticleLocators.IMAGE_URL].split("/")[-1] for url in \
                self.soup.select(ArticleLocators.IMAGES_LIST)]
            
    def download_images(self):
        """Downloads all images present in the body of an article."""
        
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} `{self.images_folder}` folder created.")
        
        for url in self.images(link=True):
            content = requests.get(url).content
            filename = url.split('/')[-1]
            filepath = os.path.join(self.images_folder, filename)
            
            if not os.path.exists(filepath):
                with open(filepath, mode="wb") as file:
                    file.write(content)
                    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {filename} downloaded.")
    
        
    def save_to_csv(self):
        """Saving datas into csv file."""
        
        datas = {
            'id': self._id,
            'url': self.url,
            'title': self.title,
            'author': self.author,
            'date': self.date(timestamp=False),
            'article_body': self.article_body,
            'redactors': self.redactors,
            'number_of_comments': self.number_of_comments,
            'image_names': repr(self.images(link=False)),
            'image_links': repr(self.images(link=True))
        }
        
        # Writing the headers when creating the file.
        if not os.path.exists(self.datas_csv):
            with open(self.datas_csv, "w") as f:
                w = csv.DictWriter(f, fieldnames=list(datas.keys()))
                w.writeheader()
        
        with open(self.datas_csv, "a") as f:
            w = csv.DictWriter(f, fieldnames=list(datas.keys()))
            w.writerow(datas)
            
            
        return datas
    
    def download_all(self):
        """
        The function downloads all images and writes the data to a csv file.
        Returns a dictionary containing the main attributes of the article :
        - id
        - title
        - author
        - article body
        - redactors
        - number of comments
        - image names
        - image links
        """
        
        self.download_images()
        self.save_to_csv()
        
        return {
            'id': self._id,
            'url': self.url,
            'title': self.title,
            'author': self.author,
            'date': self.date(timestamp=False),
            'article_body': self.article_body,
            'redactors': self.redactors,
            'number_of_comments': self.number_of_comments,
            'image_names': self.images(link=False),
            'image_links': self.images(link=True)
        }