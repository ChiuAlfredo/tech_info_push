
import json
from urllib.parse import urlparse
import re
import pandas as pd
from util.Hp_util import get_page_json, create_directory, get_content, get_product_info, get_product_disclaim, read_json, save_json, check_is_crawl, check_is_crawl_path,data_to_excel_docking,data_to_excel_desktop,data_to_excel_laptop




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
        
        self.is_crawl_web_url = check_is_crawl(f'./data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json',self.file_name)
        self.is_crawl_content = check_is_crawl_path(f'./data/hp/{self.file_name}_content/',self.file_name)
        self.is_crawl_disclaim = check_is_crawl_path(f'./data/hp/{self.file_name}_disclaim/',self.file_name)
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
            self.product_claim = read_json(f'./data/hp/{self.file_name}_disclaim/')
            return self.product_claim
        else:
            pass
    # 讀取product_content
    def get_all_product_data(self):
        if self.is_crawl_content:
            self.all_product_data = read_json(f'./data/hp/{self.file_name}_content/')
            return self.all_product_data
        else:
            pass
    
    # 讀取web_url
    def get_web_url_list(self):
        if self.is_crawl_web_url:
            with open(f'./data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            self.web_url_list = data['url']
            return data['url']
        else:
            pass

    # 讀取product_price
    def get_prodct_price(self):
        if self.is_crawl_web_url:
            with open(f'./data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.product_price = data['price']
            return data['price']
        else:
            pass
    
    # 讀取product_name
    def get_product_name(self):
        if self.is_crawl_web_url:
            with open(f'./data/hp/{self.file_name}/{self.file_name}_{self.total_pages}.json', 'r', encoding='utf-8') as f:
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
            create_directory(f'./data/hp/{self.file_name}/')
            get_content(keyword=self.keyword,total_page_number=self.total_pages,file_name=self.file_name,**kwargs)
            # self.is_crawl = True
            self.is_crawl_web_url = True
            self.get_prodct_price() 
            self.get_product_name()
            self.get_web_url_list()
            
            

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
            self.product_claim = read_json(f'./data/hp/{self.file_name}_disclaim/')
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
            self.all_product_data = read_json(f'./data/hp/{self.file_name}_content/')
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
        for n,i in enumerate(self.data_list):
            # n=0
            # i = self.data_list[n]
            self.data_list[n]['Web Link'] = self.web_url_list[n]
            self.data_list[n]['Official Price'] = self.product_price[n]
            self.data_list[n]['product_name'] = self.product_name[n]
            

        save_json(self.data_list,f'./data/hp/{self.file_name}_product.json')
    
    # 合併資料 laptop
    def combine_data_laptop(self):
        # 遍歷 data_list 中的每個字典
        for item in self.data_list:
            for key, value in item.items():
                if isinstance(value, list) and len(value) == 1:
                    item[key] = value[0]
                
        for n,i in enumerate(self.web_url_list):
            # n=0
            # i = self.data_list[n]
            self.data_list[n]['Web Link'] = self.web_url_list[n]
            self.data_list[n]['Official Price'] = self.product_price[n]
            self.data_list[n]['product_name'] = self.product_name[n]
            self.data_list[n]['disclaim'] = self.data_list_claim[n]
        
        
        # product_list =zip(self.web_url_list,self.product_price,self.product_name,self.data_list,self.data_list_claim)
        # self.product_list = list(product_list)
        save_json(self.data_list[:n],f'./data/hp/{self.file_name}_product.json')
        

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
data_to_excel_desktop()

        
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
data_to_excel_laptop()



hp_docking = hp_crawl(keyword='docking')
hp_docking.get_web_url()
hp_docking.get_data_normal()
hp_docking.get_disclaim_normal()
hp_docking.clean()
hp_docking.clean_disclaim()
hp_docking.combine_data_laptop()
data_to_excel_docking

# try_time()
