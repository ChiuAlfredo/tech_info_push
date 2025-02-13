import logging
from util.Samsung_util import crawl_product, crawl_detail, crawl_compar, detail_laptop
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Samsung.log', encoding='utf-8', level=logging.INFO)

class samsungCrawler():
    def __init__(self,keyword, company): 
        self.keyword = keyword
        self.company = company
    
    def get_product_link(self):
        crawl_product(self.company, self.keyword)
    
    def get_product_detail(self):
        crawl_detail(self.company, self.keyword)
        crawl_compar(self.company, self.keyword)
    
    def get_product_data(self):
        detail_laptop(self.company, self.keyword)


keyword_list =['laptop','desktop','docking']
keyword = keyword_list[0]
company = "Samsung"
samsung = samsungCrawler(keyword, "Samsung")
samsung.get_product_link()
samsung.get_product_detail()
samsung.get_product_data()