import requests
import json
import os 
import glob
from urllib.parse import urlparse
from joblib import Parallel, delayed
import re


import time
from functools import wraps

# 計算時間
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} took {elapsed_time:.2f} seconds to run.")
        return result
    return wrapper

# 獲取搜尋也面資訊
def get_page_json(page_number,keyword,**kwargs):
    # get page info 
    url = "https://essearchapi-na.hawksearch.com/api/v2/search"

    payload = {
    "query": "type:product",
    "ClientData": {
        "VisitId": "394bbe69-22cc-4975-82df-0a1fad7e3114",
        "VisitorId": "91e30d9a-9dfb-4dfc-8ce2-1198c18496c3",
        "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Custom": {}
    },
    "Keyword": keyword,
    "PageNo": page_number,
    "ClientGuid": "bdeebee3d2b74c8ea58522bb1db61f8e"
    }
    payload.update(kwargs)
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    # print(response.text)

    json_data = json.loads(response.text)
    
    return json_data

# 建立資料夾
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
# 儲存json       
def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
# web_url = hp_lap.web_url_list[0]

# 獲取商品資訊
def get_product_info(web_url,file_name,n):

    web_keyword = urlparse(web_url).path.split('/')[-1]

    url = f"https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2F{web_keyword}/async"
    proxies = {'https':'https://185.171.54.35:4153',
               'http':'https://185.171.54.35:4153'}
    payload = {}
    headers = {
    'Origin': 'https://www.hp.com',
    'Referer': 'https://www.hp.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(web_keyword)
    
    json_data = json.loads(response.text)
    
    # 連線錯誤重新連線
    try:
        while 'Critical content mssing'  in json_data['errors'][0]['message']:
            response = requests.request("POST", url, headers=headers, data=payload)

            print(web_keyword)
            json_data = json.loads(response.text)
    except:
        pass
    
    create_directory(f'data/hp/{file_name}_content/')
    save_json(json_data,f'data/hp/{file_name}_content/{n}.json')
    return json_data

# 獲取商品disclaim
def get_product_disclaim(web_url,file_name,n):

    web_keyword = urlparse(web_url).path.split('/')[-1]

    url = f"https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2F{web_keyword}/footerLinks"
    proxies = {'https':'https://185.171.54.35:4153',
               'http':'https://185.171.54.35:4153'}
    payload = {}
    headers = {
    'Origin': 'https://www.hp.com',
    'Referer': 'https://www.hp.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(web_keyword)
    
    json_data = json.loads(response.text)
    
    try:
        while 'Critical content mssing'  in json_data['errors'][0]['message']:
            response = requests.request("POST", url, headers=headers, data=payload)

            print(web_keyword)
            
            json_data = json.loads(response.text)
    except:
        pass
    
    create_directory(f'data/hp/{file_name}_disclaim/')
    save_json(json_data,f'data/hp/{file_name}_disclaim/{n}.json')
    return json_data



# 獲取商品內頁
def get_content(keyword,total_page_number,file_name,**kwargs):
    all_url=[]
    price =[]
    product_name =[]
    page_number = 1
    for page_number in range(1,total_page_number+1):
        json_data = get_page_json(page_number=page_number,keyword=keyword,**kwargs)
        
        all_data_list = [i['Document']for i in json_data['Results']]
        print(page_number)
        print(len(all_data_list))
        all_url.extend([i['pdp_url'][0] for i in all_data_list])
        part_price = []
        for i in all_data_list:
            try:
                part_price.append(i['cg_gs'][0])
            except:
                print(i['catentry_id'][0])
            
                catentryId  = 3074457345620840821
                catentryId =  i['catentry_id'][0]
                
                url = f"https://www.hp.com/us-en/shop/HPServices?_=1699849583399&action=pid&catentryId={catentryId}&modelId=&storeId=10151&catalogId=10051&langId=-1"
                headers = {
                    'Referer': 'https://www.hp.com/us-en/shop/sitesearch',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                }

                response = requests.request("GET", url,headers=headers)

                json_data = json.loads(response.text)
                
                price_one = json_data['priceData'][0]['gsPrice']
                part_price.append(price_one)
        price.extend(part_price)
        product_name.extend([i['product_name'][0] for i in all_data_list])
    create_directory(f'data/hp/{file_name}/')
    
    dict_data = {'url':all_url,'price':price,'product_name':product_name}
    save_json(dict_data, f'data/hp/{file_name}/{file_name}_{total_page_number}.json')
    
# keyword = 'Laptops'
# page_number = 8
# json_data = get_page_json(page_number=page_number,keyword=keyword)
    

# 檢查檔案是否存在
def check_is_crawl(file_path,file_name):
    if os.path.isfile(file_path):
        return True
    else:
        return False

# 檢查路徑是否存在‘
def check_is_crawl_path(file_path,file_name):
    if os.path.exists(file_path):
        return True
    else:
        return False


# Custom sort function
def sort_key(file):
    # Extract the number from the filename
    number = int(re.search(r'\d+', file).group())
    return number

# Read all JSON files from the directory
def read_json(file_path):
    # Get a list of all JSON files in the directory
    json_files = sorted(glob.glob(f'{file_path}/*.json'), key=sort_key)


    # Initialize an empty list to store the data
    data = []

    # Loop over all files and read them into a Python object
    for file in json_files:
        with open(file, 'r') as f:
            data.append(json.load(f))
            
    return data

# file_path = f'data/hp/{hp_desk.file_name}_content'



class hp_crawl():
    def __init__(self,keyword,name='' ,**kwargs):
        self.keyword = keyword
        self.name = name
        self.file_name = f"{self.keyword}_{self.name}"
        
        self.page_info = self.get_page_info(**kwargs)
        self.all_product_data = None
        self.total_rows = self.get_total_rows()
        self.total_pages = self.get_total_pages()
        self.product_list = None
        
        self.is_crawl_web_url = check_is_crawl(f'data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json',self.file_name)
        self.is_crawl_content = check_is_crawl_path(f'data/hp/{self.file_name}_content/',self.file_name)
        self.is_crawl_disclaim = check_is_crawl_path(f'data/hp/{self.file_name}_disclaim/',self.file_name)
        if self.is_crawl_web_url:
            self.web_url_list = self.get_web_url_list()
            self.all_product_data = self.get_all_product_data()
            self.product_price = self.get_prodct_price()
            self.product_name = self.get_product_name()
            
        else:
            self.web_url_list = None
            self.all_product_data = None
            self.product_price = None
            self.product_name = None
            
        if self.is_crawl_content:
            self.product_claim =self.get_product_claim()
        if self.is_crawl_disclaim:
            self.product_claim = self.get_product_claim()
        else:
            self.product_claim = None
    
    # 讀取product_disclaim
    def get_product_claim(self):
        if self.is_crawl_content:
            self.product_claim = read_json(f'data/hp/{self.file_name}_disclaim/')
            return self.product_claim
        else:
            pass
    # 讀取product_content
    def get_all_product_data(self):
        if self.is_crawl_content:
            self.all_product_data = read_json(f'data/hp/{self.file_name}_content/')
            return self.all_product_data
        else:
            pass
    
    # 讀取web_url
    def get_web_url_list(self):
        if self.is_crawl_web_url:
            with open(f'data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json', 'r') as f:
                data = json.load(f)
        
            self.web_url_list = data['url']
            return data['url']
        else:
            pass

    # 讀取product_price
    def get_prodct_price(self):
        if self.is_crawl_web_url:
            with open(f'data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json', 'r') as f:
                data = json.load(f)
                
            self.product_price = data['price']
            return data['price']
        else:
            pass
    
    # 讀取product_name
    def get_product_name(self):
        if self.is_crawl_web_url:
            with open(f'data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json', 'r') as f:
                data = json.load(f)
                
            self.product_name = data['product_name']
            return data['product_name']
        else:
            pass
    
    # 獲取頁面數量資訊
    def get_page_info(self,**kwargs):
            return get_page_json(page_number=1,keyword=self.keyword,**kwargs)['Pagination']
    # 獲取總共商品數量
    def get_total_rows(self):   
            return self.page_info['NofResults']
    # 獲取總共頁面數量
    def get_total_pages(self):
            return self.page_info['NofPages']
    # 讀取資料
    def load_data(self):
        self.web_url_list = self.get_web_url_list()
        self.all_product_data = None
        self.product_price = self.get_prodct_price()
        self.product_name = self.get_product_name()
        
    # 爬取web_url
    def get_web_url(self,**kwargs):
        if self.is_crawl_web_url:
            pass
        else:
            create_directory(f'data/hp/{self.file_name}/')
            get_content(keyword=self.keyword,total_page_number=self.total_pages,file_name=self.file_name,**kwargs)
            # self.is_crawl = True
            self.is_crawl_web_url = True
            self.get_prodct_price() 
            self.get_product_name()
            self.get_web_url_list()
            
            
    # 爬取product_content，joblib未使用
    def get_data_joblib(self):
        if self.is_crawl_content:
            pass
        else:
            self.load_data()
            web_link = self.web_url_list
            self.all_product_data = Parallel(n_jobs=-1)(delayed(get_product_info)(i,self.file_name,n) for n,i in enumerate(web_link))
                
        # all_product_data_spec = [i['data']['page']['pageComponents']['pdpTechSpecs']['technical_specifications'] for i in all_product_data]
    # 爬取product_content，單筆獲取
    def get_data_normal(self):
        if self.is_crawl_content:
            pass
        else:
            
            web_link = self.web_url_list
            all_product_data = [get_product_info(i,self.file_name,n) for n,i in enumerate(web_link)]
            self.all_product_data  =all_product_data
            self.is_crawl_content = True
            # all_product_data_spec = [i['data']['page']['pageComponents']['pdpTechSpecs']['technical_specifications'] for i in all_product_data]
    # 爬取product_disclaim，單筆獲取
    def get_disclaim_normal(self):
        if self.is_crawl_disclaim:
            pass
        else:
            web_link = self.web_url_list
            all_product_claim_data = [get_product_disclaim(i,self.file_name,n) for n,i in enumerate(web_link)]
            self.product_claim  =all_product_claim_data

            # all_product_data_spec = [i['data']['page']['pageComponents']['pdpTechSpecs']['technical_specifications'] for i in all_product_data]

    # 清理product_data
    def clean(self):
        if self.is_crawl_content:
            self.all_product_data = read_json(f'data/hp/{self.file_name}_content/')
        all_product_data_spec = []
        for i in self.all_product_data:
            try:
                all_product_data_spec.append(i['data']['page']['pageComponents']['pdpTechSpecs']['technical_specifications'])
            except:
                all_product_data_spec.append([])

        data_list = []
        for i in all_product_data_spec:
            new_dict = {}
            if i is []:
                new_dict.update({})
            else:
                for n in i :
                    new_dict.update({n['name']:n['value'][0]['value']})
            
            data_list.append(new_dict)
        
        self.data_list = data_list
    
    # 清理product_disclaim
    def clean_disclaim(self):
        if self.is_crawl_disclaim:
            self.product_claim = read_json(f'data/hp/{self.file_name}_disclaim/')
        all_product_claim_data = []
        for i in self.product_claim:
            try:
                all_product_claim_data.append(i['data']['page']['pageComponents']['pdpFootnotesDisclaimer'])
            except:
                all_product_claim_data.append([])

        data_list_claim = []
        for i in all_product_claim_data:
            new_dict = {}
            if i is None:
                continue
            for n in i :
                new_dict.update({n['section']:n['disclaimerPoints']})
            
            data_list_claim.append(new_dict)
        
        self.data_list_claim = data_list_claim
    
    # 清理product_data laptop
    def clean_laptop(self):
        if self.is_crawl_content:
            self.all_product_data = read_json(f'data/hp/{self.file_name}_content/')
        all_product_data_spec = []
        for i in self.all_product_data:
            try:
                all_product_data_spec.append(i['data']['page']['pageComponents']['pdpTechSpecs']['technical_specifications'])
            except:
                all_product_data_spec.append([])

        data_list = []
        for i in all_product_data_spec:
            new_dict = {}
            if i is []:
                new_dict.update({})
                continue
            else:
                for n in i :
                    if len(n['value'][0]['value'])!=1:
                        new_dict.update({n['name']:n['value'][0]['value']})
                    else:
                        new_dict.update({n['name']:n['value'][0]['value'][0]})
            
            data_list.append(new_dict)
        
        self.data_list = data_list
    
    # 合併資料
    def combine_data(self):
        product_list =zip(self.web_url_list,self.product_price,self.product_name,self.data_list)
        self.product_list = list(product_list)
        save_json(self.product_list,f'data/hp/{self.file_name}_product.json')
    
    # 合併資料 laptop
    def combine_data_laptop(self):
        product_list =zip(self.web_url_list,self.product_price,self.product_name,self.data_list,self.data_list_claim)
        self.product_list = list(product_list)
        save_json(self.product_list,f'data/hp/{self.file_name}_product.json')
        

# @timing_decorator
# def try_time():
        
hp_work_desk = hp_crawl(keyword='workstation',name = 'Desktops',FacetSelections={"dte_facet_category": ["Desktops"]})
hp_work_desk.get_web_url(FacetSelections={"dte_facet_category": ["Desktops"]})
hp_work_desk.get_data_normal()
hp_work_desk.get_disclaim_normal()
hp_work_desk.clean()
hp_work_desk.clean_disclaim()
hp_work_desk.combine_data_laptop()

hp_desk = hp_crawl(keyword='Desktops')
hp_desk.get_web_url()
hp_desk.get_data_normal()
hp_desk.get_disclaim_normal()
hp_desk.clean()
hp_desk.clean_disclaim()
hp_desk.combine_data_laptop()

        
hp_lap = hp_crawl(keyword='Laptops')
hp_lap.get_web_url()
hp_lap.get_data_normal()
hp_lap.get_disclaim_normal()
hp_lap.clean()
hp_lap.clean_disclaim()
hp_lap.combine_data_laptop()

hp_lap = hp_crawl(keyword='workstation',name = 'Laptops',FacetSelections={"dte_facet_category": ["Laptops"]})
hp_lap.get_web_url(FacetSelections={"dte_facet_category": ["Laptops"]})
hp_lap.get_data_normal()
hp_lap.get_disclaim_normal()
hp_lap.clean_laptop()
hp_lap.clean_disclaim()
hp_lap.combine_data_laptop()



hp_docking = hp_crawl(keyword='docking')
hp_docking.get_web_url()
hp_docking.get_data_normal()
hp_docking.get_disclaim_normal()
hp_docking.clean()
hp_docking.clean_disclaim()
hp_docking.combine_data_laptop()

# try_time()



