from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import json 
import pandas as pd
import random


class Web():
    def __init__(self):
        self.web_number = 0
        self.driver = self.web_driver()
    
    def web_driver(self):
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        option.add_argument('--window-size=1920,1080') 
        option.add_argument("--enable-javascript")
        option.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
        prefs = {  
        'profile.default_content_setting_values' :  {  
            'notifications' : 2  
        }  
        }  
        option.add_experimental_option('prefs',prefs)
        option.add_argument('blink-settings=imagesEnabled=false') 
        option.add_argument('--disable-gpu') 
        
        proxy = pd.read_csv('proxyscrape_premium_http_proxies.txt', delimiter='\t', encoding='utf-8',header=None)
        proxy_data = proxy.values.tolist()
        
        new_ip = random.choice(proxy_data)[0]
            #隨機選擇一個代理
        random_proxy = new_ip

        option.add_argument("--proxy-server=http://"+random_proxy)
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        return driver
    
    def get(self,url):
        
        if self.web_number == 50:
            self.driver.quit()
            self.driver = self.web_driver()
            self.web_number = 0
            self.driver.get(url)
        else:
            self.web_number = self.web_number + 1
            self.driver.get(url)
    
    def execute_script(self,script,*args):
        self.driver.execute_script(script,*args)
        
    def get_pagesource(self):
        return self.driver.page_source
    
    def find_elements(self,by,selector):
        return self.driver.find_elements(by,selector)
    def quit(self):
        self.driver.quit()
    


def add_hp_cookie(driver):
    with open(f"hp-cookie_postman.json", 'r') as file:
        data_list = json.load(file)
        
    for i in data_list:
        driver.add_cookie(i)
    
    return driver



def get_cookie(driver):
    # 指定你想要读取的JSON文件名
    file_name = 'hp_cookie_login.json'

    with open(file_name, 'w') as file:
        json.dump(driver.get_cookies(), file, indent=4) 


