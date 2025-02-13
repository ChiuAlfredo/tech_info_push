import requests

from bs4 import BeautifulSoup
import json
import pandas as pd
from tqdm import tqdm
import re 
import json

def search_crawl(keyword, company): 
    if keyword =='docking':
        search_link = "https://www.apple.com:443/us/search/adapter-%26dock?src=serp"
    else:
        search_link = f'https://www.apple.com:443/us/search/{keyword}'
    burp0_url = search_link
    burp0_cookies = {"as_sfa": "Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE", "geo": "TW", "at_check": "true", "dssf": "1", "as_dc": "ucp3", "as_atb": "1.0|MjAyNC0wNy0zMSAxMTo0MDoxMg|c3765df0f80c3f97c50b447b82e52b3f162c851d", "s_fid": "3ECEBE5D8F14999A-170BEBC0BDC4081E", "s_cc": "true", "as_pcts": "FKHT9LmcdQKN-zvDOHz9KfNd:qZkYr+OvoQZuQjRmX+wJK_X2-wB83xuas2Fr1rkdi-LfpD-0qB6ownQYvIuIcwSH8i-n2H2Dqx1YA+WenpYnk1L3yxudpcYoKjHQamn+UrYUekGP7jXF5sFp5_pHWoaY1cDKUy0bi9hv1Zev01E9SDU+", "s_vi": "[CS]v1|335596E6E8ED491C-400003AF01F24A00[CE]", "mbox": "session#22732d4e1e764977a0d96287bfe85b56#1722496274|PC#22732d4e1e764977a0d96287bfe85b56.32_0#1722496214", "dssid2": "bede219f-3d29-46de-9606-f6a4e191426c", "as_rumid": "4d35bd50-0cfb-4899-9b7d-673d08cb53fb", "pt-dm": "v1~x~g8syfzvz~m~3~n~AOS%3A%20Product%20Details%20-%20Satechi%20Multiport%20Pro%20Adapter%20V2~r~aos%3Ashop"}
    burp0_headers = {"Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "zh-TW", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}
    response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    soup = BeautifulSoup(response.content, "html.parser")
    
    products_list = []
    articles_soup = soup.select('div.rf-producttile')
    
    for article_soup in articles_soup:
        # article_soup = articles_soup[0] 
        product = {}
        product["Model Name"] = article_soup.select_one("h2.rf-producttile-name").get_text(strip=True)
        product["Web Link"] = 'https://www.apple.com'+article_soup.select_one("h2.rf-producttile-name>a")["href"]
        product["Price"] = article_soup.select_one("span.rf-producttile-pricecurrent").get_text(strip=True)
        products_list.append(product)
        
    with open(f"./data/{company}/{keyword}_search.json", "w") as f:
        json.dump(products_list, f)

def detail_crawl(keyword, company):
    with open(f"./data/{company}/{keyword}_search.json", "r") as f:
        products_list = json.load(f)

    product_detail_list = []
    error_link = []
    for product in tqdm(products_list):
        # product = products_list[0]
        try:
            burp0_url = product["Web Link"]
            burp0_headers = {"Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "zh-TW", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i", "Connection": "keep-alive"}
            requests.get(burp0_url, headers=burp0_headers)

            response = requests.get(burp0_url, headers=burp0_headers)
            soup = BeautifulSoup(response.content, "html.parser")

            product_soup = soup.select('div.rc-pdsection-panel')

            spect_dict = {}
            for i in product_soup:
                try:
                    # i = product_soup[-1]
                    spect_dict[i.select_one("h3.rc-pdsection-title").get_text(strip=True).lower()] = i.select_one(
                        "div.rc-pdsection-mainpanel"
                    ).get_text(strip=True)
                except:
                    pass
            
            product_detail_list.append({**product, **spect_dict})
            
        except Exception as e:
            print(e)
            error_link.append(**product)

    with open(f"./data/{company}/{keyword}_detail_list.json", "w") as f:
        json.dump(product_detail_list, f)
    with open(f"./data/{company}/{keyword}_error_list.json", "w") as f:
        json.dump(error_link, f)
        


def detail_crawl_laptop_desktop(keyword, company):

    burp0_url = "https://www.apple.com:443/macbook-air/compare/?modelList=Mac-studio-2022,MacBook-Air-M3"
    burp0_cookies = {"as_sfa": "Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE", "geo": "TW", "at_check": "true", "dssf": "1", "as_dc": "ucp3", "as_atb": "1.0|MjAyNC0wNy0zMSAxMTo0MDoxMg|c3765df0f80c3f97c50b447b82e52b3f162c851d", "s_cc": "true", "as_pcts": "FKHT9LmcdQKN-zvDOHz9KfNd:qZkYr+OvoQZuQjRmX+wJK_X2-wB83xuas2Fr1rkdi-LfpD-0qB6ownQYvIuIcwSH8i-n2H2Dqx1YA+WenpYnk1L3yxudpcYoKjHQamn+UrYUekGP7jXF5sFp5_pHWoaY1cDKUy0bi9hv1Zev01E9SDU+", "dssid2": "bede219f-3d29-46de-9606-f6a4e191426c", "as_rumid": "4d35bd50-0cfb-4899-9b7d-673d08cb53fb", "pt-dm": "v1~x~g8syfzvz~m~3~n~aos%3Asearch%3Aaccessories~r~aos%3Asearch"}
    burp0_headers = {"Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "zh-TW", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}
    response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    
    soup = BeautifulSoup(response.content, "html.parser")
    rows_soup = soup.select('div#backport-data>div.backport-group.compare-section')
    
    product_dict={}
    for row_soup in rows_soup:
        # row_soup = rows_soup[10]
        # 1= row_soup_3
        # print(row_soup.select_one('div[data-type="specs"]'))
        in_rows_soup = row_soup.select('div.backport-row')
        
        if len(in_rows_soup) == 1 :
            if all(cls in row_soup.get('class', []) for cls in ['backport-group', 'compare-section', 'css-sticky']):
                product_dict['Model Name'] = [i.get_text(strip=True).split('\n')[0] for i in row_soup.select('div[data-type="products"]') ]
            else:
                specs = in_rows_soup[0].select_one('div[data-type="specs"]').get_text(strip=True).lower()
                # feature = in_row_soup[0].select_one('div[data-type="features"]').get_text(strip=True).lower()
                value = [i.get_text(strip=True) for i in in_rows_soup[0].select('div.backport-row>div[data-type="featureItems"]')]
                product_dict[f'{specs}'] = value
        elif len(in_rows_soup) > 1:    
            specs = in_rows_soup[0].select_one('div[data-type="specs"]').get_text(strip=True).lower()
            dict_in_row = {}
            for in_row_soup in in_rows_soup:
                # in_row_soup = in_rows_soup[4]
                feature = in_row_soup.select_one('div[data-type="features"]').get_text(strip=True).lower()
                value = [i.get_text(strip=True) for i in in_row_soup.select('div.backport-row>div[data-type="featureItems"]')]
                for i,v in enumerate(value):
                    try:
                        dict_in_row[feature][i] = dict_in_row[feature][i]+value[i]
                    except:
                        dict_in_row[feature] = value
                
            if list(dict_in_row.keys()) == ['']:
                dict_in_row[f'{specs}'] = dict_in_row.pop('')
                
                
            product_dict.update(dict_in_row)
    

    # 定義目標長度
    target_length = len(product_dict["Model Name"])

    # 找出長度不是 34 的鍵
    invalid_keys = [key for key, value in product_dict.items() if len(value) != target_length]

    for key in invalid_keys:
        product_dict.pop(key)

    
    # 将 product_dict 转换为包含字典的列表
    product_detail_list = []
    keys = product_dict.keys()
    length = len(next(iter(product_dict.values())))  # 获取任意一个列表的长度

    for i in range(length):
        # print(i)
        product = {}
        for key in keys:
            print(key)
            product[key] = product_dict[key][i]
        product_detail_list.append(product)
    with open(f"./data/{company}/{keyword}_detail_list.json", "w") as f:
        json.dump(product_detail_list, f,ensure_ascii=False, indent=4)
        
def price_crawl(keyword, company):
    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)
        
    price_product_list = []
    for product in product_detail_list:
        # product = product_detail_list[0]
        if product['price']!='':
            
            pattern = r'\{([^}]+)\}'
            match = re.findall(pattern,  product['price'])[0]
            
            price_product_list.append(match)
    burp0_url = f"https://www.apple.com:443/us/shop/mcm/product-price?parts="
    for price_product in price_product_list:
        burp0_url += price_product+"%2C"
    burp0_cookies = {"as_sfa": "Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE", "geo": "TW", "at_check": "true", "dssf": "1", "as_dc": "ucp3", "as_atb": "1.0|MjAyNC0wNy0zMSAxMTo0MDoxMg|c3765df0f80c3f97c50b447b82e52b3f162c851d", "s_cc": "true", "as_pcts": "FKHT9LmcdQKN-zvDOHz9KfNd:qZkYr+OvoQZuQjRmX+wJK_X2-wB83xuas2Fr1rkdi-LfpD-0qB6ownQYvIuIcwSH8i-n2H2Dqx1YA+WenpYnk1L3yxudpcYoKjHQamn+UrYUekGP7jXF5sFp5_pHWoaY1cDKUy0bi9hv1Zev01E9SDU+", "dssid2": "bede219f-3d29-46de-9606-f6a4e191426c", "as_rumid": "4d35bd50-0cfb-4899-9b7d-673d08cb53fb", "pt-dm": "v1~x~g8syfzvz~m~3~n~aos%3Asearch%3Aaccessories~r~aos%3Asearch"}
    burp0_headers = {"Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.apple.com/macbook-air/compare/?modelList=Mac-studio-2022,MacBook-Air-M3", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
    response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

    data= response.json()
    
    price_list = []
    for item_key, item_value in data['items'].items():
        print(item_value['id'])
        item_id = item_value['id']
        try: 
            price = item_value['price']['value']
        except:
            price = None
        price_list.append({'id':item_id,'Official Price':price})
        
    with open(f"./data/{company}/{keyword}_price_list.json", "w") as f:
        json.dump(price_list, f,ensure_ascii=False, indent=4)
        
def detail_laptop_desktop(keyword, company):
    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)
    
    with open(f"./data/{company}/{keyword}_price_list.json", "r") as f:
        price_list = json.load(f)

    df_laptop = pd.DataFrame(product_detail_list)
    df_laptop.to_csv(f"./data/{company}/{keyword}_detail_list.csv",encoding='utf-8-sig')
    
    ports_columns_list =     [
       'thunderbolt',
       'usb	hdmi',
       'ethernet',
       'sdxc',
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

    df_laptop["Ports & Slots"] = df_laptop.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )
    
    df_laptop["Camera"] = df_laptop["camera"]

    df_laptop["Display"] = df_laptop["display"]
    df_laptop["Primary Battery"] = df_laptop[
        [
            "battery",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)
    
    df_laptop["Processor"] = df_laptop[
        [
            "chip",
            "processor"
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)
    
    df_laptop["Graphics Card"] = df_laptop["gpu"]
    
    df_laptop["Hard Drive"] = df_laptop["storage"].str.split('storage3').str[0].str.replace('Up to', '', regex=False).str.strip()
    
    df_laptop["Memory"] = df_laptop[["memory"]].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    df_laptop["Operating System"] = 'MAC OS'
    
    df_laptop["Audio and Speakers"] = df_laptop["stereo"]
    
    def extract_dimension(text,dimension_type):
        
        if dimension_type=='Depth':
            dimension_type_alt = ""
            catch_order = 3
        elif dimension_type=='Width':
            dimension_type_alt = ""
            catch_order = 2
        elif dimension_type=='Height':
            dimension_type_alt = ""
            catch_order = 0
            
            
            
        text = str(text)
        # print(text)
        if text == "nan":
            return None
        pattern = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*mm(?:\s*-\s*(\d+\.?\d*)\s*mm)?"
        match = re.search(pattern, text, re.IGNORECASE)

        pattern_cm = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*cm(?:\s*-\s*(\d+\.?\d*)\s*cm)?"
        match_cm = re.search(pattern_cm, text, re.IGNORECASE)

        pattern_len = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*mm(?:\s*-\s*(\d+\.?\d*)\s*mm)?"
        match_len = re.search(pattern_len, text, re.IGNORECASE)
        
        pattern_in = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*in(?:\s*-\s*(\d+\.?\d*)\s*in)?"
        match_in = re.search(pattern_in, text, re.IGNORECASE)
        

        if match:
            return float(match.group(1))
        elif match_cm:
            return float(match_cm.group(1)) * 10
        elif match_len:
            return float(match_len.group(1))
        elif match_in:
            return float(match_in.group(1)) * 25.4
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*mm"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[catch_order])
        return None

    def extract_weight(text):

        text = str(text).lower()
        # print(text)
        if text == "nan":
            return None
        pattern = r".*?(\d+\.?\d*)\s*kg(?:\s*-\s*(\d+\.?\d*)\s*kg)?"
        match = re.search(pattern, text, re.IGNORECASE)
        
        pattern_oz = r".*?(\d+\.?\d*)\s*oz(?:\s*-\s*(\d+\.?\d*)\s*oz)?"
        match_oz = re.search(pattern_oz, text, re.IGNORECASE)

        if match:
            if match.group(2):
                return min(float(match.group(1)), float(match.group(2)))
            return float(match.group(1))
        elif match_oz:
            if match_oz.group(2):
                return min(float(match_oz.group(1)) * 0.0283495, float(match_oz.group(2)) * 0.0283495)
            return float(match_oz.group(1)) * 0.0283495
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*kg"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[0])

        return None


    df_laptop["Height(mm)"] = df_laptop["height"].apply(lambda x: extract_dimension(x, "Height"))
    df_laptop["Width(mm)"] = df_laptop["width"].apply(lambda x: extract_dimension(x, "Width"))
    df_laptop["Depth(mm)"] = df_laptop["depth"].apply(lambda x: extract_dimension(x, "Depth"))

    df_laptop["Weight(kg)"] = df_laptop["weight"].apply(extract_weight)
    
    df_laptop["WWAN"] = None

    df_laptop["NFC"] = None
    
    def set_fpr(row):
        # 检查'fingerprint reader'字段是否为'yes'
        if "Touch" in row["secure authentication"]:
            return "Yes"

        else:
            return None


    df_laptop["FPR"] = df_laptop.apply(set_fpr, axis=1)
    df_laptop["FPR_model"] = None
    
    df_laptop["Power Supply"] = df_laptop["power and battery5"]
    
    df_laptop['dynamic-price-proxy'] = df_laptop['dynamic-price-proxy'].str.replace('{', '').str.replace('}', '')
    for item in price_list:
        # item = price_list[0]
        # Check if the ID exists in df_laptop["price"]
        if item['id'] in df_laptop['dynamic-price-proxy'].values:
            index = df_laptop[df_laptop['dynamic-price-proxy'] == item['id']].index
            # Update the corresponding row in df_laptop
            df_laptop.loc[index, 'Official Price'] = item['Official Price']

    df_laptop['Official Price'] = df_laptop['Official Price']
    df_laptop["Type"] = None
    df_laptop["Brand"] = company
    df_laptop["Web Link"] = 'https://www.apple.com/macbook-air/compare/?modelList=MacBook-Air-M3,MacBook-Pro-14-M3x'

    df = df_laptop
    
    df_laptop = df[df['Model Name'].str.contains('MacBook')]
    # 指定要输出的字段列表
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
    df_laptop[columns_to_output].to_csv(
        f"./data/{company}/{keyword}.csv", encoding="utf-8-sig", index=False
    )
    
    df_desktop = df[~df['Model Name'].str.contains('MacBook')]
    keyword = 'desktop'
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
    df_desktop[columns_to_output].to_csv(
        f"./data/{company}/{keyword}.csv", encoding="utf-8-sig", index=False
    )
        
            

def detail_docking(keyword, company):
    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_docking = pd.DataFrame(product_detail_list)

    # df_docking.to_csv(f"./data/{company}/{keyword}_detail_list.csv",encoding='utf-8-sig')


    df_docking["Ports & Slots"] = df_docking['highlights']
    def extract_weight(text):

        text = str(text).lower()
        # print(text)
        if text == "nan":
            return None
        pattern = r"Weight.*?(\d+\.?\d*)\s*kg(?:\s*-\s*(\d+\.?\d*)\s*kg)?"
        match = re.search(pattern, text, re.IGNORECASE)
        
        pattern_oz = r"Weight.*?(\d+\.?\d*)\s*oz(?:\s*-\s*(\d+\.?\d*)\s*oz)?"
        match_oz = re.search(pattern_oz, text, re.IGNORECASE)
        
        pattern_lbs = r"Weight.*?(\d+\.?\d*)\s*lb(?:\s*-\s*(\d+\.?\d*)\s*lb)?"
        match_lbs = re.search(pattern_lbs, text, re.IGNORECASE)

        if match:
            if match.group(2):
                return min(float(match.group(1)), float(match.group(2)))
            return float(match.group(1))
        elif match_oz:
            if match_oz.group(2):
                return min(float(match_oz.group(1)) * 0.0283495, float(match_oz.group(2)) * 0.0283495)
            return float(match_oz.group(1)) * 0.0283495
        elif match_lbs:
            if match_lbs.group(2):
                return min(float(match_lbs.group(1)) * 0.453592, float(match_lbs.group(2)) * 0.453592)
            return float(match_lbs.group(1)) * 0.453592
        
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*kg"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[0])

        return None
    df_docking['Dimensions & Weight'] = df_docking[
        [
            'tech specs'
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)
    
    df_docking["Weight(kg)"] = df_docking["Dimensions & Weight"].apply(extract_weight)
    
    def extract_power_delivery(power_str):
        # Regular expression to find the numeric value followed by "W"
        match = re.search(r'Power Delivery up to (\d+)\s*W', power_str, re.IGNORECASE)
        if match:
            # Extract the numeric value
            power_watts = match.group(1)
            return f"{power_watts}W"
        else:
            # Return None if no match is found
            return None
        
    df_docking["Power Supply"] = df_docking[
        [
            "highlights",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)
    df_docking['Power Supply'] = df_docking['Power Supply'].apply(extract_power_delivery)

    df_docking["Brand"] = company

    df_docking["Official Price"] = df_docking["Price"]
    df_docking['Type'] = ""
    
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
    df_docking[columns_to_output].to_csv(
        f"./data/{company}/{keyword}.csv", encoding="utf-8-sig", index=False
    )

    df_docking = df_docking[columns_to_output]
    return df_docking


        
        
keyword_list = ["laptop", "desktop", "docking"]
company = "Apple"

for keyword in keyword_list:
    # keyword = keyword_list[0]
    
    
    if keyword == "laptop" :
        detail_crawl_laptop_desktop(keyword, company)
        price_crawl(keyword, company)
        detail_laptop_desktop(keyword, company)
    if keyword == "desktop":
        pass

    if keyword == "docking":
        search_crawl(keyword, company)
        detail_crawl(keyword, company)
        detail_docking(keyword, company)