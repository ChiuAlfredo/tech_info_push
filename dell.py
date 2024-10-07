import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from requests.exceptions import TooManyRedirects
from util.Dell_util import search_crawl, detail_crawl, detail_crawl_more, detail_laptop, detail_desktop, detail_docking

class DellCrawler:
    def __init__(self,keyword, company):
        self.keyword = keyword
        self.company = company
    def get_product_link(self):
        search_crawl(self.keyword, self.company)
    
    def get_product_detail(self):
        detail_crawl(self.keyword, self.company)
        detail_crawl_more(self.keyword, self.company)
    
    def get_product_data(self):
        if self.keyword == "laptop":
            detail_laptop(self.keyword, self.company)
        elif self.keyword == "desktop":
            detail_desktop(self.keyword, self.company)
        elif self.keyword == "docking":
            detail_docking(self.keyword, self.company)
        else:
            print("keyword is not in the list")
            
            
keyword_list = ["laptop", "desktop", "docking"]
company = "Dell"
for keyword in keyword_list:
    dell = DellCrawler(keyword, company)
    dell.get_product_link()
    dell.get_product_detail()
    dell.get_product_data()
    # time.sleep(5)
