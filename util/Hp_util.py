import requests
import json
import os 
import glob
from urllib.parse import urlparse
from joblib import Parallel, delayed
import re
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


# import time
# from functools import wraps

# # 計算時間
# def timing_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         start_time = time.perf_counter()
#         result = func(*args, **kwargs)
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         print(f"Function {func.__name__} took {elapsed_time:.2f} seconds to run.")
#         return result
#     return wrapper

# 獲取搜尋也面資訊
def get_page_json(page_number,keyword,**kwargs):
    # get page info 
    # url = "https://essearchapi-na.hawksearch.com/api/v2/search"
    url = 'https://hp.searchapi-na.hawksearch.com/api/v2/search'

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
# https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2Fhp-laptop-17t-cn300-173-7p3q0av-1/footerLinks
    payload = {}
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "Tracestate": "3043875@nr=0-1-3043875-601394608-869c2273437acd8a----1728305079416", "Traceparent": "00-7dfe3a36b5c3009eda5de38187e6621d-869c2273437acd8a-01", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwNDM4NzUiLCJhcCI6IjYwMTM5NDYwOCIsImlkIjoiODY5YzIyNzM0MzdhY2Q4YSIsInRyIjoiN2RmZTNhMzZiNWMzMDA5ZWRhNWRlMzgxODdlNjYyMWQiLCJ0aSI6MTcyODMwNTA3OTQxNn19", "Accept": "application/json, text/plain, */*", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.hp.com/us-en/shop/pdp/hp-laptop-17t-cn300-173-7p3q0av-1", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}

    response = requests.request("POST", url, headers=burp0_headers, data=payload)

    print(web_keyword)
    
    json_data = json.loads(response.text)
    
    # 連線錯誤重新連線
    try:
        while 'Critical content mssing'  in json_data['errors'][0]['message']:
            response = requests.request("POST", url, headers=burp0_headers, data=payload)

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
    # headers = {
    # 'Origin': 'https://www.hp.com',
    # 'Referer': 'https://www.hp.com/',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    # }
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "Tracestate": "3043875@nr=0-1-3043875-601394608-869c2273437acd8a----1728305079416", "Traceparent": "00-7dfe3a36b5c3009eda5de38187e6621d-869c2273437acd8a-01", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwNDM4NzUiLCJhcCI6IjYwMTM5NDYwOCIsImlkIjoiODY5YzIyNzM0MzdhY2Q4YSIsInRyIjoiN2RmZTNhMzZiNWMzMDA5ZWRhNWRlMzgxODdlNjYyMWQiLCJ0aSI6MTcyODMwNTA3OTQxNn19", "Accept": "application/json, text/plain, */*", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.hp.com/us-en/shop/pdp/hp-laptop-17t-cn300-173-7p3q0av-1", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}

    response = requests.request("GET", url, headers=burp0_headers, data=payload)

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
                try:
                    price_one = json_data['priceData'][0]['gsPrice']
                except:
                    price_one = "No money"
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
        with open(file, 'r', encoding='utf-8') as f:
            data.append(json.load(f))
            
    return data

# file_path = f'data/hp/{hp_desk.file_name}_content'



def data_to_excel_docking():
    with open('./data/hp/docking__product.json', 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
        data = json.load(file)   
    
    for i in data:
        if i['disclaim']:
            del i['disclaim']
    df = pd.DataFrame(data)
    
    df['Type'] = df['product_name'].apply(lambda x: 'Chrome' if 'chrome' in x.lower() else 'Workstation' if 'workstation' in x.lower() else 'Gaming' if 'omen' in x.lower() or 'victus' in x.lower() else 'Commercial' if 'thin client' in x.lower() or 'pro' in x.lower() or 'elite' in x.lower() or 't550' in x.lower() else 'Consumer' if 'pavilion' in x.lower() or 'envy' in x.lower() else 'None Type_DT')
    
    
    ports_columns_list = [
        "External Ports Location 01",
        "External Ports 01",
        "External Ports Location 02",
        'External Ports 02',
        'External Ports Location 03',
        'External Ports 03'
        
    ]

    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }

    df["Ports & Slots"] = df.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )

    df['Power Supply'] = df['Power supply'].apply(lambda x: x if pd.notna(x) else None)

    def extract_and_convert_to_kg(weight_str):
        if pd.notna(weight_str):
        
            match = re.search(r"(\d+(\.\d+)?)\s*lb", weight_str)
            if match:
                weight_lb = float(match.group(1))
                weight_kg = round(weight_lb * 0.45359237, 2)
                return weight_kg
            return None
        return None

    
    df["Weight(kg)"] = df["Weight"].apply(extract_and_convert_to_kg)
    
    df['Brand'] = "Hp"
    
    df['Model Name'] = df['product_name']
    
    

    columns_to_output = [
        "Type",
        "Brand",
        "Model Name",
        "Official Price",
        "Ports & Slots",
        "Weight(kg)",
        "Power Supply",
        "Web Link",

    ]
    df[columns_to_output].to_csv(
        f"./data/hp/docking.csv", encoding="utf-8-sig", index=False
    )
    
        
    

def data_to_excel_desktop():
    json_data = ['./data/hp/Desktops__product.json','./data/hp/workstation_Desktops_product.json']

    with open(json_data[0], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
        data_1 = json.load(file)   
    
    with open(json_data[1], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
        data_2 = json.load(file)   
        
    data = data_1 + data_2
    
    for i in data:
        if i['disclaim']:
            del i['disclaim']
    df = pd.DataFrame(data)
    
    df['Type'] = df['product_name'].apply(lambda x: 'Chrome' if 'chrome' in x.lower() else 'Workstation' if 'workstation' in x.lower() else 'Gaming' if 'omen' in x.lower() or 'victus' in x.lower() else 'Commercial' if 'thin client' in x.lower() or 'pro' in x.lower() or 'elite' in x.lower() or 't550' in x.lower() else 'Consumer' if 'pavilion' in x.lower() or 'envy' in x.lower() else 'None Type_DT')
    
    
    ports_columns_list = [
        "External I/O Ports",
        "Expansion slots",
    ]

    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }

    df["Ports & Slots"] = df.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )
    
    df['Graphics Card'] = df['Graphics'].apply(lambda x: x.split("&nbsp;")[-1].split("Integrated")[-1] if pd.notna(x) else None)
    
    df['Hard Drive'] = df['Storage']
    
    df['Operating System'] = df['Operating system'].apply(lambda x: x if pd.notna(x) else None)
    
    df['Audio and Speakers'] = df['Audio Features'].apply(lambda x: x if pd.notna(x) else None)
    
    df['Power Supply'] = df['Power supply'].apply(lambda x: x if pd.notna(x) else None)
    # Function to convert inches to centimeters
    def inches_to_cm(inches):
        return round(inches * 2.54, 2)

    # Function to extract and convert dimensions
    def convert_dimensions(dimensions):
        # dimensions = df["Dimensions (W X D X H)"][204]
        # print(dimensions)
        if pd.notna(dimensions):
            match = re.search(r"(\d+\.?\d*) x (\d+\.?\d*) x (\d+\.?\d*) in", dimensions)
            
            if match:
                width_in = float(match.group(1))
                depth_in = float(match.group(2))
                height_in = float(match.group(3))
                
                width_cm = inches_to_cm(width_in)
                depth_cm = inches_to_cm(depth_in)
                height_cm = inches_to_cm(height_in)
                
                return height_cm, width_cm, depth_cm
            
            return None, None, None
        else:
            return None, None, None
    
    df["Height(mm)"],df["Width(mm)"],df["Depth(mm)"] = zip(*df["Dimensions (W X D X H)"].apply(convert_dimensions))

    
    def extract_and_convert_to_kg(weight_str):
        if pd.notna(weight_str):
        
            match = re.search(r"(\d+(\.\d+)?)\s*lb", weight_str)
            if match:
                weight_lb = float(match.group(1))
                weight_kg = round(weight_lb * 0.45359237, 2)
                return weight_kg
            return None
        return None

    
    df["Weight(kg)"] = df["Weight"].apply(extract_and_convert_to_kg)
    
    df['Brand'] = "Hp"
    
    df['Model Name'] = df['product_name']
    
    

    columns_to_output = [
            "Type",
            "Brand",
            "Model Name",
            "Official Price",
            "Ports & Slots",
            "Display",
            "Processor",
            "Graphics Card",
            "Hard Drive",
            "Memory",
            "Operating System",
            "Audio and Speakers",
            "Height(mm)",
            "Width(mm)",
            "Depth(mm)",
            "Weight(kg)",
            "Power Supply",
            "Web Link",
        ]
    df[columns_to_output].to_csv(
        f"./data/hp/desktop.csv", encoding="utf-8-sig", index=False
    )
    
    
    
    
    
    
    

def data_to_excel_laptop():
        
    json_data = ['./data/hp/Laptops__product.json','./data/hp/workstation_Laptops_product.json']
    

    with open(json_data[0], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
        data_1 = json.load(file)   
    
    with open(json_data[1], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
        data_2 = json.load(file)   
        
    data = data_1 + data_2
    
    disclaim_list =[]
    for i in data:
        if i['disclaim']:
            disclaim_list.append(i['disclaim'])
            del i['disclaim']
    df = pd.DataFrame(data)
    
    df['Type'] = df['product_name'].apply(lambda x: 'Chrome' if 'chrome' in x.lower() else 'Workstation' if 'workstation' in x.lower() else 'Gaming' if 'omen' in x.lower() or 'victus' in x.lower() else 'Commercial' if 'thin client' in x.lower() or 'pro' in x.lower() or 'elite' in x.lower() or 't550' in x.lower() else 'Consumer' if 'pavilion' in x.lower() or 'envy' in x.lower() else 'None Type_DT')
    
    
    ports_columns_list = [
        "External I/O Ports",
        "Expansion slots",
    ]

    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }

    df["Ports & Slots"] = df.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )
    
    df['Graphics Card'] = df['Graphics'].apply(lambda x: x.split("&nbsp;")[-1].split("Integrated")[-1] if pd.notna(x) else None)
    
    df['Hard Drive'] = df['Internal drive']
    
    df['Operating System'] = df['Operating system'].apply(lambda x: x if pd.notna(x) else None)
    
    df['Audio and Speakers'] = df['Audio Features'].apply(lambda x: x if pd.notna(x) else None)
    
    df['Power Supply'] = df['Power supply'].apply(lambda x: x if pd.notna(x) else None)
    # Function to convert inches to centimeters
    def inches_to_cm(inches):
        return round(inches * 2.54, 2)

    # Function to extract and convert dimensions
    def convert_dimensions(dimensions):
        # dimensions = df["Dimensions (W X D X H)"][204]
        # print(dimensions)
        if pd.notna(dimensions):
            match = re.search(r"(\d+\.?\d*) x (\d+\.?\d*) x (\d+\.?\d*) in", dimensions)
            
            if match:
                width_in = float(match.group(1))
                depth_in = float(match.group(2))
                height_in = float(match.group(3))
                
                width_cm = inches_to_cm(width_in)
                depth_cm = inches_to_cm(depth_in)
                height_cm = inches_to_cm(height_in)
                
                return height_cm, width_cm, depth_cm
            
            return None, None, None
        else:
            return None, None, None
    
    df["Height(mm)"],df["Width(mm)"],df["Depth(mm)"] = zip(*df["Dimensions (W X D X H)"].apply(convert_dimensions))

    
    def extract_and_convert_to_kg(weight_str):
        if pd.notna(weight_str):
        
            match = re.search(r"(\d+(\.\d+)?)\s*lb", weight_str)
            if match:
                weight_lb = float(match.group(1))
                weight_kg = round(weight_lb * 0.45359237, 2)
                return weight_kg
            return None
        return None

    
    df["Weight(kg)"] = df["Weight"].apply(extract_and_convert_to_kg)
    
    df['Brand'] = "Hp"
    
    df['Model Name'] = df['product_name']
    
    df['Camera'] = df['Webcam']
    
    df['Primary Battery'] = df['Battery']
    
    df['NFC'] = None
    df['FPR_model'] = None
    for index,i in enumerate(disclaim_list):
        # index = 0
        # i = disclaim_list[index]
        specs_string = ' '.join(map(str, i['SPECS']))+' '.join(map(str, i['OVERVIEW']))+' '.join(map(str, i['FEATURES']))
        
        if '4G' in specs_string:
            # print(index)
            df.loc[index,'WWAN'] = '4G'
        elif '5G' in specs_string:
            df.loc[index,'WWAN'] = '5G'
            
        if 'NFC' in specs_string:
            df.loc[index,'NFC'] = 'Yes'
            
        if 'Fingerprint' in specs_string:
            df.loc[index,'FPR_model'] = 'Yes'
            
    df['FPR'] = df['Finger print reader'].apply(lambda x: 'No' if pd.notna(x) and 'No' in x else ('Yes' if pd.notna(x) else None))
    

    columns_to_output = [
        "Type",
        "Brand",
        "Model Name",
        "Official Price",
        "Ports & Slots",
        "Camera",
        "Display",
        "Primary Battery",
        "Processor",
        "Graphics Card",
        "Hard Drive",
        "Memory",
        "Operating System",
        "Audio and Speakers",
        "Height(mm)",
        "Width(mm)",
        "Depth(mm)",
        "Weight(kg)",
        "WWAN",
        "NFC",
        "FPR_model",
        "FPR",
        "Power Supply",
        "Web Link",
    ]
    
    
    df[columns_to_output].to_csv(
        f"./data/hp/desktop.csv", encoding="utf-8-sig", index=False
    )
    
    
    
    
    



# import pandas as pd 

# with open('data/hp/workstation_Laptops_product.json', 'r', encoding='utf-8') as f:
#     work_data = json.load(f)

# with open('data/hp/Laptops__product.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
    
# work_df = pd.DataFrame(work_data)
# df = pd.DataFrame(data)

# df_laptop = pd.concat([work_df,df],axis=0)
# df_laptop.to_csv('data/hp/hp_product.csv',index=False,encoding='utf-8-sig')


# if "Operation system" in df_laptop.columns:
#     df_laptop["Operating system"] = df_laptop["Operating system"].fillna(
#         df_laptop["Operation system"]
#     )
# # df_laptop["Model Name"] = df_laptop["Model Name"].fillna(df_laptop["product_name"])
# df_laptop["Brand"] = "Hp"

# # Function to remove the specified HTML snippets
# def clean_html_snippets(text):
#     if isinstance(text, float):
#         return text
#     # Define a more general regex pattern to match any content within the square brackets
#     html_snippet = r"<a class='footerLink' href='#disclaimerTabs'>\[\d+(,\d+)*\]</a>"
#     return re.sub(html_snippet, '', text)

# # Apply the function to the DataFrame
# df_laptop["Ports & Slots"] = df_laptop["External I/O Ports"].apply(clean_html_snippets)






# df_laptop["Camera"] = (
#     df_laptop["Webcam"] 
# )
# def consolidate_row_columns(row, columns_list):
#     # 检查指定的列是否全部为NaN
#     if all(pd.isna(row[col]) for col in columns_list if col in row):
#         return None
#     else:
#         # 返回一个字典，仅包含非NaN的列名和值
#         return {
#             col: row[col]
#             for col in columns_list
#             if col in row and not pd.isna(row[col])
#         }





# df_laptop["Display"] = df_laptop["Display"]

# df_laptop["Primary Battery"] = df_laptop["Battery"]

# df_laptop["Processor"] = df_laptop[
#     [
#         "processor type",
#         "processor model",
#         "processor speed",
#         "processor speed (turbo)",
#         "processor core",
#     ]
# ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)

# df_laptop["graphics"].fillna(df_laptop["graphics controller model"], inplace=True)
# graphics_columns_list = [
#     "graphics controller manufacturer",
#     "graphics",
#     "graphics memory capacity",
#     "graphics memory technology",
#     "graphics memory accessibility",
# ]
# df_laptop["Graphics Card"] = df_laptop[graphics_columns_list].apply(
#     lambda x: ", ".join(x.dropna().astype(str)), axis=1
# )

# df_laptop["Hard Drive"] = df_laptop["total solid state drive capacity"]

# df_laptop["Memory"] = df_laptop["standard memory"] + df_laptop["memory technology"]

# df_laptop["Operating System"] = df_laptop["operating system"]

# df_laptop["Audio and Speakers"] = df_laptop.apply(
#     consolidate_row_columns,
#     axis=1,
#     columns_list=["hd audio", "speakers", "number of speakers	speaker output mode"],
# )

# def check_network_type(value):
#     # Normalize the case for consistent matching
#     value = str(value).lower()
#     if "4G" in value and "5G" in value:
#         return "4G/5G"
#     elif "4G" in value:
#         return "4G"
#     elif "5G" in value:
#         return "5G"
#     else:
#         return None  # or 'Not Available', depending on your preference

# df_laptop["WWAN"] = df_laptop["Wireless technology"].apply(check_network_type)
# df_laptop["FPR"] = df_laptop["Finger print reader"].str.contains("Fingerprint sensor")
# df_laptop["FPR_model"] = None
# df_laptop["Power Supply"] = df_laptop["Power supply"].str.extract(
#     r"(\d+)\s*W external AC"
# )


# def inch_to_mm(inch):
#     try:
#         return round(float(inch) * 25.4, 2)
#     except:
#         return None

# # Function to extract width, depth, and height
# def extract_dimensions(dimensions):
#     if isinstance(dimensions, float):
#         return None, None, None
#     match = re.search(r"(\d+\.?\d*) x (\d+\.?\d*) x (\d+\.?\d*) ", dimensions)
#     if match:
#         width = float(match.group(1))
#         depth = float(match.group(2))
#         height = float(match.group(3))
#         return width, depth, height
#     return None, None, None

# # Convert all values to strings and apply the function to the DataFrame
# df_laptop['Dimensions (W X D X H)'] = df_laptop['Dimensions (W X D X H)'].astype(str)
# df_laptop[['width', 'depth', 'height']] = df_laptop['Dimensions (W X D X H)'].apply(
#     lambda x: pd.Series(extract_dimensions(x))
# )

# df_laptop["Height(mm)"] = df_laptop["height"].apply(inch_to_mm)
# df_laptop["Width(mm)"] = df_laptop["width"].apply(inch_to_mm)
# df_laptop["Depth(mm)"] = df_laptop["height"].apply(inch_to_mm)

# def convert_to_kg(weight_str):
#     weight_str = 'Starting at 4.5 lb'
#     # print(weight_str)
#     weight_str = str(weight_str).lower()
#     # 定义正则表达式
   
#     # 定义正则表达式
#     lbs_pattern = re.compile(r"(\d+(\.\d+)?)\s*lb")

#     # 匹配lbs和kg
#     lbs_match = lbs_pattern.search(weight_str)  # Use search instead of match
#     if lbs_match:
#         return round(float(lbs_match.group(1)) * 0.45359237, 2)  # U


#     # 如果没有匹配到任何单位，返回None
#     return None


# df_laptop["Weight(kg)"] = df_laptop["Weight"].apply(convert_to_kg)


# laptop_columns = [
#     "Brand",
#     "Model Name",
#     "Official Price",
#     "Ports & Slots",
#     "Camera",
#     "Display",
#     "Primary Battery",
#     "Processor",
#     "Graphics Card",
#     "Hard Drive",
#     "Memory",
#     "Operating System",
#     "Audio and Speakers",
#     "Height(mm)",
#     "Width(mm)",
#     "Depth(mm)",
#     "Weight(kg)",
#     "WWAN",
#     "NFC",
#     "FPR",
#     "FPR_model",
#     "Power Supply",
#     "Web Link",
# ]

# df_laptop[laptop_columns].to_excel("./Asus/laptop.xlsx", header=False)


# def desktop_data(keyword):
# # laptop
# with open("./Asus/desktop_detail_list.json", "r") as f:
#     product_detail_list = json.load(f)

# combined_dicts = [
#     {k: v for d in sublist for k, v in d.items()} for sublist in product_detail_list
# ]

# df = pd.DataFrame(combined_dicts)
# df["Brand"] = "Asus"
# df["Official Price"] = None
# df["Ports & Slots"] = df["rear i/o ports"] + df["side i/o ports"]
# df.rename(
#     columns={
#         "display": "Display",
#         "processor": "Processor",
#         "graphics": "Graphics Card",
#         "storage": "Hard Drive",
#         "memory": "Memory",
#         "operating system": "Operating System",
#         "audio": "Audio and Speakers",
#         "power supply": "Power Supply",
#     },
#     inplace=True,
# )

# df = dim_transform(df)
# df = weight_transform(df)

# columns = [
#     "Brand",
#     "Model Name",
#     "Official Price",
#     "Ports & Slots",
#     "Display",
#     "Processor",
#     "Graphics Card",
#     "Hard Drive",
#     "Memory",
#     "Operating System",
#     "Audio and Speakers",
#     "Height(mm)",
#     "Width(mm)",
#     "Depth(mm)",
#     "Weight(kg)",
#     "Power Supply",
#     "Web Link",
# ]

# df[columns].to_excel("./Asus/desktop.xlsx")