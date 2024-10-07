import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import pandas as pd
import logging
from util.Asus_util import search_crawl, crawl_detail, laptop_data, desktop_data, docking_data
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Asus.log', encoding='utf-8', level=logging.INFO)

class asus_crawl():
    def __init__(self, keyword, company):
        self.keyword = keyword
        self.company = company
    
    def get_product_link(self):
        search_crawl(self.keyword)
        
    def get_product_detail(self):
        crawl_detail(self.keyword)
        
    def get_product_data(self):
        if self.keyword == "laptop":
            laptop_data(self.keyword)
        elif self.keyword == "desktop":
            desktop_data(self.keyword)
        elif self.keyword == "docking":
            docking_data(self.keyword)
        else:
            print("keyword is not in the list")

keyword_list = ["laptop", "desktop", "docking"]

for keyword in keyword_list:
    # keyword = 'laptop'
    asus = asus_crawl(keyword, "Asus")
    asus.get_product_link()
    asus.get_product_detail()
    asus.get_product_data()
    # time.sleep(5)


