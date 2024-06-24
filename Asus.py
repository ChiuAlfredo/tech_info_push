import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

keyword = "laptop"


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
    return product_link_list


product_link_list = search_crawl(keyword)
# 網址不會重複
product_link_list = list(set(product_link_list))


# Write the JSON data to a file
with open(f"./Asus/{keyword}_search.json", "w") as f:
    json.dump(product_link_list, f)


# %%

# Open the JSON file and load the data
with open(f"./Asus/{keyword}_search.json", "r") as f:
    product_link_list = json.load(f)


def check_value_lengths(spec_dict):
    lengths = {len(v) for v in spec_dict.values()}
    if len(lengths) > 1:
        return 0
        print("Values in spec_dict have different lengths.")
    else:
        return len(next(iter(spec_dict.values())))


def dict_to_list(spec_dict, col_num=0):
    result_list = []
    for i in range(col_num):
        dict_list = []
        for key in spec_dict.keys():
            dict_list.append({key: spec_dict[key][i]})
        result_list.append(dict_list)

    return result_list


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


def dim_transform(spec_dict):
    if "dimensions (w x d x h)" in spec_dict:
        # 處理demension
        spec_dict["Width(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[0]) * 10, 2)
            for i in spec_dict["dimensions (w x d x h)"]
        ]
        spec_dict["Depth(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[1]) * 10, 2)
            for i in spec_dict["dimensions (w x d x h)"]
        ]
        spec_dict["Height(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[2]) * 10, 2)
            for i in spec_dict["dimensions (w x d x h)"]
        ]
    elif "weight and dimensions" in spec_dict:
        # 處理demension
        spec_dict["Width(mm)"] = [
            round(
                float(
                    re.search(r"Height:\s*(\d+\.?\d*\s*cm)", i, re.IGNORECASE).group(1)
                )
                * 10,
                2,
            )
            for i in spec_dict["weight and dimensions"]
        ]
        spec_dict["Depth(mm)"] = [
            round(
                float(
                    re.search(r"Width:\s*(\d+\.?\d*\s*cm)", i, re.IGNORECASE).group(1)
                )
                * 10,
                2,
            )
            for i in spec_dict["weight and dimensions"]
        ]
        spec_dict["Height(mm)"] = [
            round(
                float(
                    re.search(r"Depth:\s*(\d+\.?\d*\s*cm)", i, re.IGNORECASE).group(1)
                )
                * 10,
                2,
            )
            for i in spec_dict["weight and dimensions"]
        ]

    elif "dimensions(w x d x h)" in spec_dict:
        # 處理demension
        spec_dict["Width(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[0]) * 10, 2)
            for i in spec_dict["dimensions(w x d x h)"]
        ]
        spec_dict["Depth(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[1]) * 10, 2)
            for i in spec_dict["dimensions(w x d x h)"]
        ]
        spec_dict["Height(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[2]) * 10, 2)
            for i in spec_dict["dimensions(w x d x h)"]
        ]
    elif "dimensions" in spec_dict:
        spec_dict["Width(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[0]), 2)
            for i in spec_dict["dimensions"]
        ]
        spec_dict["Depth(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[1]), 2)
            for i in spec_dict["dimensions"]
        ]
        spec_dict["Height(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[2]), 2)
            for i in spec_dict["dimensions"]
        ]
    elif "dimensions (esti.)" in spec_dict:
        spec_dict["Width(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[0]) * 10, 2)
            for i in spec_dict["dimensions (esti.)"]
        ]
        spec_dict["Depth(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[1]) * 10, 2)
            for i in spec_dict["dimensions (esti.)"]
        ]
        spec_dict["Height(mm)"] = [
            round(float(re.findall(r"(\d+\.?\d+)", i, re.IGNORECASE)[2]) * 10, 2)
            for i in spec_dict["dimensions (esti.)"]
        ]
    else:
        print(spec_dict.keys())
    return spec_dict


def rog_crawl(soup):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(".ProductSpec__specProductNameWrapper__J0OSb")
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select(
        ".ProductSpec__row__wSwCC.ProductSpec__spec__IjTyl.ProductSpec__productSpecList__JERh3"
    )
    for i in operation_soup:
        # i = operation_soup[0]
        key = (
            i.select(".ProductSpec__productSpecItemTitle__JVvSd")[0]
            .text.strip()
            .lower()
        )
        values_soup = i.select(".ProductSpec__rowItem__hGYWS")
        value = [i.text.strip() for i in values_soup]
        if "" in value:
            value = [i.text.strip() for i in values_soup if i.text.strip() != ""] * len(
                values_soup
            )
        # 特例處理 3個產品,但是都是同樣規格

        if key != "":
            spec_dict[key] = value

    spec_dict = weight_transform(spec_dict)

    spec_dict = dim_transform(spec_dict)

    col_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * col_num

    return dict_to_list(spec_dict, col_num)


def home_work_creators(soup):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(".LevelFourProductPageHeader__modelName__70ttK")[0]
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select(".TechSpec__rowTable__1LR9D")
    for i in operation_soup:
        # i = operation_soup[3]
        if i.select(".TechSpec__rowTableTitle__3GLj4") != []:
            key = i.select(".TechSpec__rowTableTitle__3GLj4")[0].text.strip().lower()
            values_soup = i.select(".TechSpec__rowTableItemBox__8tmQd")
            value = [i.text.strip() for i in values_soup]

            if key != "":
                spec_dict[key] = value

    spec_dict = weight_transform(spec_dict)

    spec_dict = dim_transform(spec_dict)

    col_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * col_num

    return dict_to_list(spec_dict, col_num)


def zenbook_14_crawl(soup):
    spec_dict = {}
    # 載入網頁
    product_name_soup = soup.select(".LevelFourProductPageHeader__modelName__70ttK")[0]
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]
    spec_dict["Model Name"] = product_names_list

    # 剩下的全部一起爬
    operation_soup = soup.select(".insoweTable>section")
    for i in operation_soup:
        # i = operation_soup[1]
        if i.select(".insoweCol.insoweCol1") != []:
            key = i.select(".insoweCol.insoweCol1")[0].text.strip().lower()
            values_soup = i.select(".insoweCol.insoweCol2")
            value = [i.text.strip() for i in values_soup]

            if key != "":
                spec_dict[key] = value

    # 處理重量
    # Kg
    # 匹配重量
    spec_dict = weight_transform(spec_dict)
    spec_dict = dim_transform(spec_dict)

    col_num = check_value_lengths(spec_dict)
    spec_dict["Web Link"] = [link] * col_num
    return dict_to_list(spec_dict, col_num)


def TUF_crawl(soup):
    spec_dict = {}

    product_name_soup = soup.select(".LevelFourProductPageHeader__modelName__70ttK")[0]
    product_names_list = [
        " ".join(i.text.strip().replace("\n", "").split()) for i in product_name_soup
    ]

    # 剩下的全部一起爬
    operation_soup = soup.select(".productSpecItems>div")
    for i in operation_soup:
        # i = operation_soup[1]
        if i.select(".itemTitle.itemTitle1") != []:
            key = i.select(".itemTitle.itemTitle1")[0].text.strip().lower()
            values_soup = i.select(".rowItems")
            value = [i.text.strip() for i in values_soup]
            # 刪除空字符
            value = [v for v in value if v != ""]

            if key != "":
                spec_dict[key] = value

    col_num = check_value_lengths(spec_dict)

    spec_dict = weight_transform(spec_dict)

    spec_dict = dim_transform(spec_dict)

    spec_dict["Web Link"] = [link] * col_num

    spec_dict["Model Name"] = [product_names_list[0] + i for i in spec_dict["model"]]

    return dict_to_list(spec_dict, col_num)


import time

start_time = time.time()

# product_link_list=product_link_list[:100]
product_detail_list = []
error_link = []
for link in tqdm(product_link_list):
    print(link)
    # link = product_link_list[13]
    # link  = 'https://www.asus.com/Laptops/For-Gaming/TUF-Gaming/ASUS-TUF-Gaming-A15-2024/'

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
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.select(".ProductSpec__specProductNameWrapper__J0OSb") != []:
                result_list = rog_crawl(soup)
                product_detail_list.extend(result_list)

        elif "bag" not in link:
            burp0_url = link + "/techspec/"
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
            soup = BeautifulSoup(response.content, "html.parser")

            if soup.select(".TechSpec__rowTableTitle__3GLj4") != []:
                result_list = home_work_creators(soup)
                product_detail_list.extend(result_list)
            elif soup.select(".insoweTable>section") != []:
                result_list = zenbook_14_crawl(soup)
                product_detail_list.extend(result_list)
            elif soup.select(".productSpecItems>div") != []:
                result_list = TUF_crawl(soup)
                product_detail_list.extend(result_list)

        else:
            print("no fit")
            error_link.append(link)
    except:
        error_link.append(link)

end_time = time.time()

print("Execution time: ", end_time - start_time, "seconds")

with open("./Asus/laptop_detail_list.json", "w") as f:
    json.dump(product_detail_list, f)

with open("./Asus/laptop_error_link_list.json", "w") as f:
    json.dump(error_link, f)

# %%
# desktop
import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

keyword = "desktop"


product_link_list = search_crawl(keyword)
# 網址不會重複
product_link_list = list(set(product_link_list))


# Write the JSON data to a file
with open(f"./Asus/{keyword}_search.json", "w") as f:
    json.dump(product_link_list, f)


# %%

# Open the JSON file and load the data
with open(f"./Asus/{keyword}_search.json", "r") as f:
    product_link_list = json.load(f)


product_link_list = product_link_list[:50]
product_detail_list = []
error_link = []

for link in tqdm(product_link_list):
    print(link)
    # link = product_link_list[0]
    # link  = 'https://www.asus.com/Displays-Desktops/All-in-One-PCs/Everyday-use/ASUS-AIO-A5702WVAR/'

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
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.select(".ProductSpec__specProductNameWrapper__J0OSb") != []:
                result_list = rog_crawl(soup)
                product_detail_list.extend(result_list)

        elif "bag" not in link:
            burp0_url = link + "/techspec/"
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
            soup = BeautifulSoup(response.content, "html.parser")

            if soup.select(".TechSpec__rowTableTitle__3GLj4") != []:
                result_list = home_work_creators(soup)
                product_detail_list.extend(result_list)
            elif soup.select(".insoweTable>section") != []:
                result_list = zenbook_14_crawl(soup)
                product_detail_list.extend(result_list)
            elif soup.select(".productSpecItems>div") != []:
                result_list = TUF_crawl(soup)
                product_detail_list.extend(result_list)

        else:
            print("no fit")
            error_link.append(link)
    except:
        error_link.append(link)

with open("./Asus/desktop_detail_list.json", "w") as f:
    json.dump(product_detail_list, f)

with open("./Asus/desktop_error_link_list.json", "w") as f:
    json.dump(error_link, f)
# %%
# desktop
import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

keyword = "docking"


product_link_list = search_crawl(keyword)
# 網址不會重複
product_link_list = list(set(product_link_list))


# Write the JSON data to a file
with open(f"./Asus/{keyword}_search.json", "w") as f:
    json.dump(product_link_list, f)


# %%

# Open the JSON file and load the data
with open(f"./Asus/{keyword}_search.json", "r") as f:
    product_link_list = json.load(f)


product_detail_list = []
error_link = []

for link in tqdm(product_link_list):
    print(link)
    # link = product_link_list[2]
    # link  = 'https://www.asus.com/Displays-Desktops/All-in-One-PCs/Everyday-use/ASUS-AIO-A5702WVAR/'

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
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.select(".ProductSpec__specProductNameWrapper__J0OSb") != []:
                result_list = rog_crawl(soup)
                product_detail_list.extend(result_list)

        elif "bag" not in link:
            burp0_url = link + "/techspec/"
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
            soup = BeautifulSoup(response.content, "html.parser")

            if soup.select(".TechSpec__rowTableTitle__3GLj4") != []:
                result_list = home_work_creators(soup)
                product_detail_list.extend(result_list)
            elif soup.select(".insoweTable>section") != []:
                result_list = zenbook_14_crawl(soup)
                product_detail_list.extend(result_list)
            elif soup.select(".productSpecItems>div") != []:
                result_list = TUF_crawl(soup)
                product_detail_list.extend(result_list)

        else:
            print("no fit")
            error_link.append(link)
    except:
        error_link.append(link)

with open("./Asus/docking_detail_list.json", "w") as f:
    json.dump(product_detail_list, f)

with open("./Asus/docking_error_link_list.json", "w") as f:
    json.dump(error_link, f)


# %%
# laptop
# 轉換成csv
import pandas as pd
import json

# laptop
with open("./Asus/laptop_detail_list.json", "r") as f:
    product_detail_list = json.load(f)

combined_dicts = [
    {k: v for d in sublist for k, v in d.items()} for sublist in product_detail_list
]

df_laptop = pd.DataFrame(combined_dicts)
# 處理同樣欄位不同名稱
df_laptop["operating system"] = df_laptop["operating system"].fillna(
    df_laptop["operation system"]
)
df_laptop["Model Name"] = df_laptop["Model Name"].fillna(df_laptop["product_name"])
df_laptop["Brand"] = "Asus"
df_laptop["Official Price"] = None
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
laptop_columns=[
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
    "Weight(kg)"
]


df_laptop[laptop_columns].transpose().to_excel("./Asus/laptop.xlsx", header=False)

# %%
# desktop
import pandas as pd
import json

# laptop
with open("./Asus/desktop_detail_list.json", "r") as f:
    product_detail_list = json.load(f)

combined_dicts = [
    {k: v for d in sublist for k, v in d.items()} for sublist in product_detail_list
]

df = pd.DataFrame(combined_dicts)
# 處理同樣欄位不同名稱
# df['operating system'] = df['operating system'].fillna(df['operation system'])
# df['Model Name'] = df['Model Name'].fillna(df['product_name'])
df['Brand'] = 'Asus'
df['Official Price'] = None
df['Ports & Slots'] = df['rear i/o ports'] + df['side i/o ports']
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
# columns = [
#     "Model Name",
#     "operating system",
#     "processor",
#     "memory",
#     "display",
#     "graphics",
#     "storage",
#     "sata",
#     "rear i/o ports",
#     "side i/o ports",
#     "camera",
#     "audio",
#     "network and communication",
#     "power supply",
#     "Weight(kg)",
#     "Width(mm)",
#     "Depth(mm)",
#     "Height(mm)",
#     "Web Link",
# ]
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
    "Web Link"
]

df[columns].transpose().to_excel("./Asus/desktop.xlsx")
# %%
# docking
import pandas as pd
import json

# laptop
with open("./Asus/docking_detail_list.json", "r") as f:
    product_detail_list = json.load(f)

combined_dicts = [
    {k: v for d in sublist for k, v in d.items()} for sublist in product_detail_list
]

df = pd.DataFrame(combined_dicts)
# 處理同樣欄位不同名稱
# df['operating system'] = df['operating system'].fillna(df['operation system'])
# df['Model Name'] = df['Model Name'].fillna(df['product_name'])
df['Brand'] = 'Asus'
df['Official Price'] = None
df['Ports & Slots'] = df['i/o ports']
df['Power Supply'] = df['power consumption'].fillna(df['power adapter'])
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
columns = [
    "Brand",
    "Model Name",
    "Official Price",
    "Ports & Slots",
    "Power Supply",
    "Weight(kg)",
    "Web Link"
]

df[columns].transpose().to_excel("./Asus/docking.xlsx")
