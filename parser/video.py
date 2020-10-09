import os
import csv
import datetime
import functools

import requests
from bs4 import BeautifulSoup

from locators.video import VideoLocators


class VideoParser:
    def __init__(self, url):
        self.url = url
        self.datas_csv = "video_datas.csv"
    
    def html_content(self):
        "Returns HTML content"
        return requests.get(self.url).content
    
    
    @functools.cached_property
    def soup(self):
        "Returns beautifulsoup object for parsing"
        return BeautifulSoup(self.html_content(), "html.parser")
    
    @property
    def _id(self):
        return self.url.split('-')[-1].strip()
    
    def __repr__(self):
        return f'<Video(url="{self.url}" title="{self.title}" author="{self.author}" date="{self.date()}" id="{self._id}")'
    
    @property
    def title(self):
        "Returns the title of the page"
        return self.soup.select_one(VideoLocators.TITLE).text.strip()
    
    def date(self, timestamp=False):
        date = self.soup.select_one(VideoLocators.DATETIME).text.strip()
        date_object = datetime.datetime.strptime(date, "%d/%m/%Y à %H:%M")
        
        if not timestamp:
            return date_object.strftime("%d/%m/%Y %H:%M")
        else:
            return int(date_object.timestamp())
            
    @property
    def author(self):
        "Returns the author of the video"
        return self.soup.select_one(VideoLocators.AUTHOR).text.strip()
        
    @property
    def video_description(self):
        "Returns the description of the video"
        return self.soup.select_one(VideoLocators.VIDEO_DESCRIPTION).text.strip()
    
    @property
    def number_of_comments(self):
        return self.soup.select_one(VideoLocators.NUMBER_OF_COMMENTS).text.strip().split()[0]
    
    def save_to_csv(self):
        """Saving datas into csv file."""
    
        datas = {
            'id': self._id,
            'url': self.url,
            'title': self.title,
            'author': self.author,
            'date': self.date(timestamp=False),
            'video_description': self.video_description,
            'number_of_comments': self.number_of_comments,
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