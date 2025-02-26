import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import pandas as pd
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Asus.log', encoding='utf-8', level=logging.INFO)


def search_crawl(keyword):
    burp0_url = f"https://odinapi.asus.com:443/recent-data/apiv2/SearchResult?SystemCode=asus&WebsiteCode=global&SearchKey='{keyword}'&SearchType=products&SearchPDLine=&SearchPDLine2=&PDLineFilter=&TopicFilter=&CateFilter=&PageSize=900&Pages=1&LocalFlag=0&siteID=www&sitelang="
    burp0_headers = {
        "Sec-Ch-Ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://www.asus.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Priority": "u=4, i",
    }
    response = requests.get(burp0_url, headers=burp0_headers)

    # Convert the response content to JSON
    data = response.json()

    product_list = data["Result"]["List"]

    # product_list[0]
    # ['Name','ProductURL']

    product_link_list = [product["ProductURL"] for product in product_list]

    product_link_list = list(set(product_link_list))

    # Write the JSON data to a file
    with open(f"./data/Asus/{keyword}_search.json", "w") as f:
        json.dump(product_link_list, f)
    return product_link_list


def check_value_lengths(spec_dict):
    lengths = {len(v) for v in spec_dict.values()}
    return len(next(iter(spec_dict.values())))


def dict_to_list(spec_dict, product_num=0):
    result_list = []
    if product_num == 1:
        for i in range(product_num):
            i = 0
            dict_list = []
            for key in spec_dict.keys():
                try:
                    dict_list.append({key: spec_dict[key][i]})
                except:
                    print(f"{key} can add")
            result_list.append(dict_list)
    elif product_num > 1:
        for i in range(product_num):
            dict_list = []
            for key in spec_dict.keys():
                dict_list.append({key: spec_dict[key][i]})
            result_list.append(dict_list)

    return result_list


def rog_crawl(soup, link):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(".ProductSpec__specProductNameWrapper__J0OSb")
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    if '' in product_names_list:
        product_names_list = ["".join(filter(None, [name.strip() for name in product_names_list]))]
        
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select(
        ".ProductSpec__row__wSwCC.ProductSpec__spec__IjTyl.ProductSpec__productSpecList__JERh3"
    )
    for i in operation_soup:
        # i = operation_soup[3]
        key = (
            i.select(".ProductSpec__productSpecItemTitle__JVvSd")[0]
            .text.strip()
            .lower()
        )
        values_soup = i.select(".ProductSpec__rowItem__hGYWS")
        value = []
        for v in values_soup:
            text = v.select(".ProductSpec__rowItem__hGYWS>div")
            value.append(",\n ".join([i.text.strip() for i in text]))
        # values_soup[0].select('.ProductSpec__rowItem__hGYWS>div')
        # value = [i.text.strip() for i in values_soup]
        if "" in value:
            value = []
            for v in values_soup:
                text = v.select(".ProductSpec__rowItem__hGYWS>div")
                if text != []:
                    value.append(",\n ".join([i.text.strip() for i in text]))
            value = value * len(values_soup)
            # value = [i.text.strip() for i in values_soup if i.text.strip() != ""] * len(
            #     values_soup
            # )
        # 特例處理 3個產品,但是都是同樣規格

        if key != "":
            spec_dict[key] = value

    # spec_dict = weight_transform(spec_dict)

    # spec_dict = dim_transform(spec_dict)

    product_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * product_num

    return dict_to_list(spec_dict, product_num)


def rog_crawl_1(soup, link):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(
        "div.ProductSpecSingle__productSpecNameSingle__r6z\\+6"
    )
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    if '' in product_names_list:
        product_names_list = ["".join(filter(None, [name.strip() for name in product_names_list]))]
        
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select(".ProductSpecSingle__productSpecItemRow__BKwUK")

    for i in operation_soup:
        # i = operation_soup[1]
        key = (
            i.select(".ProductSpecSingle__productSpecItemTitle__HKAZq")[0]
            .text.strip()
            .lower()
        )

        # texts = [span.text for span in i.select(".ProductSpecSingle__productSpecItemContent__oJI5w>div")]

        # value  = ',\n '.join(texts)
        values_soup = i.select(".ProductSpecSingle__productSpecItemContent__oJI5w")
        value = []
        for v in values_soup:
            text = v.select(".ProductSpecSingle__productSpecItemContent__oJI5w>div")
            value.append(",\n ".join([i.text.strip() for i in text]))
        # value = [i.text.strip() for i in values_soup]
        if "" in value:
            value = []
            for v in values_soup:
                text = v.select(".ProductSpecSingle__productSpecItemContent__oJI5w>div")
                if text != []:
                    value.append(",\n ".join([i.text.strip() for i in text]))
            value = value * len(values_soup)
        # 特例處理 3個產品,但是都是同樣規格

        if key != "":
            spec_dict[key] = value

    # spec_dict = weight_transform(spec_dict)

    # spec_dict = dim_transform(spec_dict)

    product_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * product_num

    return dict_to_list(spec_dict, product_num)

def rog_crawl_2(soup, link):
    spec_dict = {}
    # 載入網頁

    product_name_soup = soup.select(".productSpec__row .nameWrapper")
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    if '' in product_names_list:
        product_names_list = ["".join(filter(None, [name.strip() for name in product_names_list]))]
    
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬

    operation_soup = soup.select(".productSpecItems .itemsFrame.dataFrame")
        
    for i in operation_soup:
        # i = operation_soup[3]
        key = (
            i.select(".itemTitle")[0]
            .text.strip()
            .lower()
        )
        values_soup = i.select(".rowItemsFrame")
        value = []
        for v in values_soup:
            text = v.select(".rowItemsFrame>div")
            value.append(",\n ".join([i.text.strip() for i in text]))
        # values_soup[0].select('.ProductSpec__rowItem__hGYWS>div')
        # value = [i.text.strip() for i in values_soup]
        if "" in value:
            value = []
            for v in values_soup:
                text = v.select(".rowItemsFrame>div")
                if text != []:
                    value.append(",\n ".join([i.text.strip() for i in text]))
            value = value * len(values_soup)
            # value = [i.text.strip() for i in values_soup if i.text.strip() != ""] * len(
            #     values_soup
            # )
        # 特例處理 3個產品,但是都是同樣規格

        if key != "":
            spec_dict[key] = value

    # spec_dict = weight_transform(spec_dict)

    # spec_dict = dim_transform(spec_dict)

    product_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * product_num

    return dict_to_list(spec_dict, product_num)



def home_work_creators(soup, link):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(".LevelFourProductPageHeader__modelName__70ttK")[0]
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    if '' in product_names_list:
        product_names_list = ["".join(filter(None, [name.strip() for name in product_names_list]))]

    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select(".TechSpec__rowTable__1LR9D")
    for i in operation_soup:
        # i = operation_soup[5]
        if i.select(".TechSpec__rowTableTitle__3GLj4") != []:
            key = i.select(".TechSpec__rowTableTitle__3GLj4")[0].text.strip().lower()
            values_soup = i.select(".TechSpec__rowTableItemBox__8tmQd")
            # value=[]
            # for v in values_soup:
            #     text = v.select(".TechSpec__rowTableItem__2QY9U>div")
            #     value.append(',\n '.join([i.text.strip() for i in text]))

            for v in values_soup:
                for br in v.find_all("br"):
                    br.replace_with("\n")
            value = [i.text.strip() for i in values_soup]

            if key != "":
                spec_dict[key] = value

    # spec_dict = weight_transform(spec_dict)

    # spec_dict = dim_transform(spec_dict)

    col_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * col_num

    return dict_to_list(spec_dict, col_num)


def zenbook_14_crawl(soup, link):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(".LevelFourProductPageHeader__modelName__70ttK")[0]
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    if '' in product_names_list:
        product_names_list = ["".join(filter(None, [name.strip() for name in product_names_list]))]
    
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select(".insoweTable>section")
    for i in operation_soup:
        # i = operation_soup[1]
        if i.select(".insoweCol.insoweCol1") != []:
            key = i.select(".insoweCol.insoweCol1")[0].text.strip().lower()
            values_soup = i.select(".insoweCol.insoweCol2")
            for v in values_soup:
                for br in v.find_all("br"):
                    br.replace_with("\n")
            # value=[]
            # for v in values_soup:
            #     text = v.select(".insoweCol.insoweCol2>div")
            #     value.append(',\n '.join([i.text.strip() for i in text]))
            value = [i.text.strip() for i in values_soup]

            if key != "":
                spec_dict[key] = value

    # 處理重量
    # Kg
    # 匹配重量
    # spec_dict = weight_transform(spec_dict)
    # spec_dict = dim_transform(spec_dict)

    col_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * col_num
    return dict_to_list(spec_dict, col_num)


def TUF_crawl(soup, link):
    spec_dict = {}

    product_name_soup = soup.select(".LevelFourProductPageHeader__modelName__70ttK")[0]
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    if '' in product_names_list:
        product_names_list = ["".join(filter(None, [name.strip() for name in product_names_list]))]

    # 剩下的全部一起爬
    operation_soup = soup.select(".productSpecItems>div")
    for i in operation_soup:
        # i = operation_soup[1]
        if i.select(".itemTitle.itemTitle1") != []:
            key = i.select(".itemTitle.itemTitle1")[0].text.strip().lower()
            values_soup = i.select(".rowItems")
            value = []
            for v in values_soup:
                text = v.select(".rowItems>div")
                value.append(",\n ".join([i.text.strip() for i in text]))
            # value = [i.text.strip() for i in values_soup]
            # 刪除空字符
            value = [v for v in value if v != ""]

            if key != "":
                spec_dict[key] = value

    col_num = check_value_lengths(spec_dict)

    # spec_dict = weight_transform(spec_dict)

    # spec_dict = dim_transform(spec_dict)

    spec_dict["Web Link"] = [link] * col_num

    spec_dict["Model Name"] = [product_names_list[0] + i for i in spec_dict["model"]]

    return dict_to_list(spec_dict, col_num)

def pro_art_crawl(soup, link):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(".text__light.spec__title")[0]
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    if '' in product_names_list:
        product_names_list = ["".join(filter(None, [name.strip() for name in product_names_list]))]
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select('div.spec__container > div.spec__content')
    for i in operation_soup:
        # i = operation_soup[4]
        if i.select(".spec__item.item-left") != []:
            key = i.select(".spec__item.item-left")[0].text.strip().lower()
            values_soup = i.select(".spec__item.item-right")
            # value=[]
            # for v in values_soup:
            #     text = v.select(".TechSpec__rowTableItem__2QY9U>div")
            #     value.append(',\n '.join([i.text.strip() for i in text]))

            for v in values_soup:
                for br in v.find_all("br"):
                    br.replace_with("\n")
            value = [i.text.strip() for i in values_soup]

            if key != "":
                spec_dict[key] = value

    # spec_dict = weight_transform(spec_dict)

    # spec_dict = dim_transform(spec_dict)

    col_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * col_num

    return dict_to_list(spec_dict, col_num)

def crawl_detail(keyword):
    # keyword = 'laptop'
    # Open the JSON file and load the data
    with open(f"./data/Asus/{keyword}_search.json", "r") as f:
        product_link_list = json.load(f)

    print(len(product_link_list))

    # product_link_list=product_link_list[:50]
    product_detail_list = []
    error_link = []
    for idx, link in enumerate(tqdm(product_link_list)):
        # link = "https://www.asus.com/Laptops/For-Home/Vivobook/ASUS-Vivobook-S-14-OLED-M5406/"
        user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)','AppleWebKit/537.36 (KHTML, like Gecko)','Chrome/58.0.3029.110 Safari/537.3','PostmanRuntime/7.37.3']
        user_agent = user_agent_list[idx % 4]
        if idx % 100 == 0 and idx != 0:
            time.sleep(20)
            
        print(link)
        # link = product_link_list[1]
        # link  = 'https://www.asus.com/Laptops/For-Creators/Vivobook/Vivobook-Pro-16X-3D-OLED-K6604/'

        # 可能會出現同個網址，一個網址要多抓多種型號
        result_list = []
        try:
            if "rog" in link and "bag" not in link:
                burp0_url = link + "/spec/"
                burp0_headers = {
                    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "zh-TW",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Origin": "https://rog.asus.com",
                    "Sec-Fetch-Site": "same-site",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Priority": "u=1, i",
                    "Connection": "keep-alive",
                }
                response = requests.get(burp0_url, headers=burp0_headers)
                # response = requests.get(burp0_url)
                soup = BeautifulSoup(response.content, "html.parser")
                if soup.select(".ProductSpec__specProductNameWrapper__J0OSb") != []:
                    result_list = rog_crawl(soup, link)
                    product_detail_list.extend(result_list)
                elif (
                    soup.select("div.ProductSpecSingle__productSpecNameSingle__r6z\\+6")
                    != []
                ):
                    result_list = rog_crawl_1(soup, link)
                    product_detail_list.extend(result_list)
                elif soup.select(".productSpec__row .nameWrapper") !=[]:
                    result_list = rog_crawl_2(soup, link)
                    product_detail_list.extend(result_list)

                else:
                    logging.info(f"no data:  {link}")
                    error_link.append(link)

                if result_list == []:
                    logging.info(f"no data:  {link}")
                    error_link.append(link)

            elif "bag" not in link:
                burp0_url = link + "/techspec/"
                burp0_cookies = {
                    "isHideFBK": "undefined",
                    "BVBRANDID": "9c1be0bf-0316-4aa5-b0b4-372a6a68cb35",
                    "isReadCookiePolicyDNT": "Yes",
                    "isReadCookiePolicyDNTAa": "true",
                    "_ga": "GA1.1.1865733467.1718724212",
                    "_fbp": "fb.1.1718724212389.254767886456035576",
                    "_gcl_au": "1.1.1066758563.1718724595",
                    "_tt_enable_cookie": "1",
                    "_ttp": "AkQ884dIH2IDoHCHiuJ29oKGxaV",
                    "_ga_VEYLYML0TC": "GS1.1.1718785365.2.1.1718786025.60.0.0",
                    "_ga_BP9E82TF15": "GS1.1.1718785365.2.1.1718786025.60.0.0",
                    "_ce.s": "v~af070468104e112cce5491e0daf7cc8b01636ee0~lcw~1718812394251~lva~1718785599819~vpv~2~v11.cs~154890~v11.s~1b755540-2e15-11ef-8c53-e154d154b7fb~v11.sla~1718785921952~v11.send~1718812394241~gtrk.la~lxm0ird7~lcw~1718812394251",
                }
                burp0_headers = {
                    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Accept-Language": "zh-TW",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-User": "?1",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Priority": "u=0, i",
                    "Connection": "keep-alive",
                }
                response = requests.get(
                    burp0_url, headers=burp0_headers, cookies=burp0_cookies
                )
                soup = BeautifulSoup(response.content, "html.parser")

                if soup.select(".TechSpec__rowTableTitle__3GLj4") != []:
                    result_list = home_work_creators(soup, link)

                elif soup.select(".insoweTable>section") != []:
                    result_list = zenbook_14_crawl(soup, link)
                elif soup.select(".productSpecItems>div") != []:
                    result_list = TUF_crawl(soup, link)
                elif soup.select(".spec__container>div") != []:
                    result_list = pro_art_crawl(soup, link)

                if "expertbook" in link:
                    burp0_url = link + ""
                    burp0_headers = {
                        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "zh-TW",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
                        "Sec-Ch-Ua-Platform": '"Windows"',
                        "Origin": "https://www.asus.com",
                        "Sec-Fetch-Site": "same-site",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Priority": "u=1, i",
                        "Connection": "keep-alive",
                    }
                    response = requests.get(burp0_url, headers=burp0_headers)

                    if "NFC" in str(response.content):
                        result_list = [i + [{"NFC": "True"}] for i in result_list]
                    else:
                        result_list = [i + [{"NFC": "False"}] for i in result_list]
                else:
                    result_list = [i + [{"NFC": "False"}] for i in result_list]

                if result_list == []:
                    logging.info(f"no data:  {link}")
                    error_link.append(link)
                else:
                    product_detail_list.extend(result_list)

            else:
                logging.info(f"it's not laptop:  {link}")
                error_link.append(link)
        except Exception as e:
            print('no')
            logging.info(f"{e}:  {link}")
            error_link.append(link)

    with open(f"./data/Asus/{keyword}_detail_list.json", "w") as f:
        print(len(product_detail_list))
        json.dump(product_detail_list, f)

    with open(f"./data/Asus/{keyword}_error_link_list.json", "w") as f:
        print(len(error_link))
        json.dump(error_link, f)


def weight_transform(spec_dict):

    if "weight and dimensions" in spec_dict:
        spec_dict["Weight(kg)"] = [
            re.search(r"Weight:\s*(\d+\.?\d*\s*kg)", i, re.IGNORECASE).group(1)
            for i in spec_dict["weight and dimensions"]
        ]

    elif "weight" in spec_dict:

        # 處理重量
        # Kg
        spec_dict["Weight(kg)"] = [
            float(re.search(r"(\d+\.?\d*)\s*(kg|g)", i, re.IGNORECASE).group(1))
            / (1000 if "kg" not in i and "Kg" not in i else 1)
            for i in spec_dict["weight"]
        ]
    elif "weight (esti.)" in spec_dict:

        spec_dict["Weight(kg)"] = [
            float(re.search(r"(\d+\.?\d*)\s*(kg|g)", i, re.IGNORECASE).group(1))
            / (1000 if "kg" not in i and "Kg" not in i else 1)
            for i in spec_dict["weight (esti.)"]
        ]

    return spec_dict


def dim_transform(df):
    # drive_columns = [col for col in df_laptop.columns if 'dimensions' in col.lower()]
    # print(drive_columns)
    # df = df_laptop
    def clean_number(s):
        if isinstance(s, (int, float)):
            return s
        return re.sub(r"[^\d.]", "", str(s))

    def extract_dimensions(value):
        if isinstance(value, (int, float)):
            return [value]
        return re.findall(r"(\d+\.?\d*)\s*(?:cm|mm)?", str(value), re.IGNORECASE)

    def process_row(row):
        for column in [
            "dimensions (w x d x h)",
            "dimensions(w x d x h)",
            "dimensions",
            "dimensions (esti.)",
            "dimensions\n                      (w x d x h)",
            "weight and dimensions"
        ]:
            if column in row.index and pd.notna(row[column]):
                dims = extract_dimensions(row[column])
                if len(dims) >= 3:
                    return pd.Series(
                        {
                            "Width(mm)": round(float(clean_number(dims[0])) * 10, 2),
                            "Depth(mm)": round(float(clean_number(dims[1])) * 10, 2),
                            "Height(mm)": round(float(clean_number(dims[2])) * 10, 2),
                        }
                    )

        if "weight and dimensions" in row.index and pd.notna(
            row["weight and dimensions"]
        ):
            value = str(row["weight and dimensions"])
            height = re.search(
                r"Height:\s*(\d+\.?\d*\s*(?:cm|mm)?)", value, re.IGNORECASE
            )
            width = re.search(
                r"Width:\s*(\d+\.?\d*\s*(?:cm|mm)?)", value, re.IGNORECASE
            )
            depth = re.search(
                r"Depth:\s*(\d+\.?\d*\s*(?:cm|mm)?)", value, re.IGNORECASE
            )
            if height and width and depth:
                return pd.Series(
                    {
                        "Width(mm)": round(
                            float(clean_number(height.group(1))) * 10, 2
                        ),
                        "Depth(mm)": round(float(clean_number(width.group(1))) * 10, 2),
                        "Height(mm)": round(
                            float(clean_number(depth.group(1))) * 10, 2
                        ),
                    }
                )

        return pd.Series({"Width(mm)": None, "Depth(mm)": None, "Height(mm)": None})

    result = df.apply(process_row, axis=1)
    return pd.concat([df, result], axis=1)


def weight_transform(df):
    def extract_weight(value):
        if pd.isna(value):
            return None
        value = str(value)

        match = re.search(r"Weight:\s*(\d+\.?\d*)\s*kg", value, re.IGNORECASE)
        if match:
            return float(match.group(1))

        match = re.search(r"(\d+\.?\d*)\s*(kg|g)", value, re.IGNORECASE)
        if match:
            weight = float(match.group(1))
            unit = match.group(2).lower()
            return weight if unit == "kg" else weight / 1000
        return None

    def process_row(row):
        if "weight and dimensions" in row.index and pd.notna(
            row["weight and dimensions"]
        ):
            return extract_weight(row["weight and dimensions"])
        elif "weight" in row.index and pd.notna(row["weight"]):
            return extract_weight(row["weight"])
        elif "weight (esti.)" in row.index and pd.notna(row["weight (esti.)"]):
            return extract_weight(row["weight (esti.)"])
        return None

    df["Weight(kg)"] = df.apply(process_row, axis=1)
    return df


def laptop_data(keyword):
    # laptop
    with open("./data/Asus/laptop_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    combined_dicts = [
        {k: v for d in sublist for k, v in d.items()} for sublist in product_detail_list
    ]

    df_laptop = pd.DataFrame(combined_dicts)

    df_laptop.to_csv("./Asus/laptop.csv", encoding="utf-8-sig")
    # 處理同樣欄位不同名稱
    if "operation system" in df_laptop.columns:
        df_laptop["operating system"] = df_laptop["operating system"].fillna(
            df_laptop["operation system"]
        )
    # df_laptop["Model Name"] = df_laptop["Model Name"].fillna(df_laptop["product_name"])
    df_laptop["Brand"] = "Asus"
    df_laptop["Official Price"] = None

    def check_network_type(value):
        # Normalize the case for consistent matching
        value = str(value).lower()
        if "4g" in value and "5g" in value:
            return "4G/5G"
        elif "4g" in value:
            return "4G"
        elif "5g" in value:
            return "5G"
        else:
            return None  # or 'Not Available', depending on your preference

    df_laptop["WWAN"] = df_laptop["network and communication"].apply(check_network_type)
    df_laptop["FPR"] = df_laptop["security"].str.contains("Fingerprint")
    df_laptop["FPR_model"] = None
    df_laptop["Power Supply"] = df_laptop["power supply"].str.extract(
        r"(\d+W AC Adapter)"
    )

    df_laptop = dim_transform(df_laptop)
    df_laptop = weight_transform(df_laptop)

    df_laptop.rename(
        columns={
            "i/o ports": "Ports & Slots",
            "camera": "Camera",
            "display": "Display",
            "battery": "Primary Battery",
            "processor": "Processor",
            "graphics": "Graphics Card",
            "storage": "Hard Drive",
            "memory": "Memory",
            "operating system": "Operating System",
            "audio": "Audio and Speakers",
        },
        inplace=True,
    )
    laptop_columns = [
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
        "FPR",
        "FPR_model",
        "Power Supply",
        "Web Link",
    ]
    
    df_laptop = df_laptop[df_laptop['Web Link'].str.contains('laptop', case=False, na=False)]

    df_laptop[laptop_columns].to_excel("./data/Asus/laptop.xlsx", header=False)


def desktop_data(keyword):
    # laptop
    with open("./data/Asus/desktop_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    combined_dicts = [
        {k: v for d in sublist for k, v in d.items()} for sublist in product_detail_list
    ]

    df = pd.DataFrame(combined_dicts)
    df["Brand"] = "Asus"
    df["Official Price"] = None
    df["Ports & Slots"] = df["rear i/o ports"] + df["side i/o ports"]
    df.rename(
        columns={
            "display": "Display",
            "processor": "Processor",
            "graphics": "Graphics Card",
            "storage": "Hard Drive",
            "memory": "Memory",
            "operating system": "Operating System",
            "audio": "Audio and Speakers",
            "power supply": "Power Supply",
        },
        inplace=True,
    )

    df = dim_transform(df)
    df = weight_transform(df)

    columns = [
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

    df[columns].to_excel("./data/Asus/desktop.xlsx")


def docking_data(keyword):
    # laptop
    with open("./data/Asus/docking_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    combined_dicts = [
        {k: v for d in sublist for k, v in d.items()} for sublist in product_detail_list
    ]

    df = pd.DataFrame(combined_dicts)
    # 處理同樣欄位不同名稱
    # df['operating system'] = df['operating system'].fillna(df['operation system'])
    # df['Model Name'] = df['Model Name'].fillna(df['product_name'])
    df["Brand"] = "Asus"
    df["Official Price"] = None
    df["Ports & Slots"] = df["i/o ports"]
    df["Power Supply"] = df["power consumption"].fillna(df["power adapter"])
    # columns = [
    #     "Model Name",
    #     "display",
    #     "i/o ports",
    #     "signal frequency",
    #     "audio feature",
    #     "power consumption",
    #     "Weight(kg)",
    #     "Width(mm)",
    #     "Depth(mm)",
    #     "Height(mm)",
    #     "Web Link",
    # ]
    df = weight_transform(df)
    columns = [
        "Brand",
        "Model Name",
        "Official Price",
        "Ports & Slots",
        "Power Supply",
        "Weight(kg)",
        "Web Link",
    ]

    df[columns].to_excel("./data/Asus/docking.xlsx")


# keyword_list = ["laptop", "desktop", "docking"]
# for keyword in keyword_list:
#     # keyword = 'desktop'
#     if keyword == "laptop":
#         product_link_list = search_crawl(keyword)

#         crawl_detail(keyword=keyword)
#         laptop_data(keyword=keyword)
#     elif keyword == "desktop":
#         product_link_list = search_crawl(keyword)
#         crawl_detail(keyword=keyword)
#         desktop_data(keyword=keyword)
#     elif keyword == "docking":
#         product_link_list = search_crawl(keyword)
#         crawl_detail(keyword=keyword)
#         docking_data(keyword=keyword)
