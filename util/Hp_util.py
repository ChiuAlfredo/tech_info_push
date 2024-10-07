import requests
import json
import os 
import glob
from urllib.parse import urlparse
from joblib import Parallel, delayed
import re
import pandas as pd
from bs4 import BeautifulSoup


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
    def process_value(value):
        if isinstance(value, list):
            v_num = 0
            v = ""
            for v_num in range(len(value)):
                v = v + '\n' +value[v_num]
            value = v
        else:
            value = value
        value = value.replace("</p></li><li><p>","\n")
        need_delete = value.split("<")    
        need=0
        delete_data = []
        for need in range(len(need_delete)):
            if ">" in need_delete[need]:
                delete_data.append(need_delete[need].split(">")[0])
        delete_data.sort()
        need=0
        for need in range(len(delete_data)):
            if need == 0:
                value = value.replace("<{}".format(delete_data[need]),"")
            else:
                value = value.replace("<{}".format(delete_data[need]),"")
        need_delete_2 = value.split("[")    
        need=0
        delete_data_2 = []
        for need in range(len(need_delete_2)):
            if "]" in need_delete_2[need]:
                delete_data_2.append(need_delete_2[need].split("]")[0])
        delete_data_2.sort()
        need=0
        for need in range(len(delete_data_2)):
            if need == 0:
                value = value.replace("[{}]".format(need_delete_2[need]),"")
            else:
                value = value.replace("[{}]".format(need_delete_2[need]),"")                
        value = value.replace(">","\n",1).replace(">","").replace("&amp;","").replace("&nbsp;","").strip()
        return value

    titles = ["Type","Brand","Model Name","Official Price","Ports & Slots","Power Supply","Weight","Web Link"]
    json_data = ['./data/hp/docking__product.json']
    print(len(json_data))
    for i in range(len(json_data)):
        # 打开JSON文件
        with open(json_data[i], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
            data = json.load(file)
        j = 0
        for D in data:
            Type,Brand,Model_Name,Official_Price,Ports_Slots,Power_Supply,Weight,Web_Link="","Hp",D[2],D[1],"","","",D[0]       
            P1,P2,P4="","",""
            
            D[3] = {key.strip(): value for key, value in D[3].items()}    
            lowercase_dict = {key.lower(): process_value(value) for key, value in D[3].items()}
            D[3] = lowercase_dict
            
            if "external ports 01" in D[3]:
                P1 = D[3]["external ports 01"]        
            if "external ports 02" in D[3]:
                P2 = D[3]["external ports 02"]        
            if "external ports 04" in D[3]:
                P4 = D[3]["external ports 04"]
            if "power supply" in D[3]:
                Power_Supply = D[3]["power supply"]
            if "weight" in D[3]:
                Weight = D[3]["weight"]
            
            Ports_Slots = P1.strip()+"\n"+P2.strip()
            Ports_Slots = Ports_Slots.strip() +"\n" +P4.strip()
            Ports_Slots = Ports_Slots.strip()
            
            if Weight != "":
                Weight_kg = float(Weight.split("lb")[0].strip())*0.4536
                Weight = round(Weight_kg,2)
            
            if len(Model_Name.split("+"))>1:
                Ports_Slots = "Web No Data"
            if len(Model_Name.split("and"))>1:
                Ports_Slots = "Web No Data"        
            j+=1    
            B = [Type,Brand,Model_Name,Official_Price,Ports_Slots,Power_Supply,Weight,Web_Link]
            A = pd.Series(titles)
            
            if i == 0 and j == 1:
                C = pd.DataFrame(B,index = A)
            else:
                B = pd.DataFrame(B,index = A)
                B.columns = [j-1]
                C = C.merge(B,how = "outer",left_index=True, right_index=True)
    C = C.T

    C['Weight(kg)'] = C['Weight']
    C = C[["Type","Brand","Model Name","Official Price","Ports & Slots","Power Supply","Weight(kg)","Web Link"]]
    C.to_csv("./data/hp/docking.csv",encoding="utf-8-sig",index = False)


def data_to_excel_desktop():
    def process_value(value):
        if isinstance(value, list):
            v_num = 0
            v = ""
            for v_num in range(len(value)):
                v = v + '\n' +value[v_num]
            value = v
        else:
            value = value
        value = value.replace("</p></li><li><p>","\n")
        need_delete = value.split("<")    
        need=0
        delete_data = []
        for need in range(len(need_delete)):
            if ">" in need_delete[need]:
                delete_data.append(need_delete[need].split(">")[0])
        delete_data.sort()
        need=0
        for need in range(len(delete_data)):
            if need == 0:
                value = value.replace("<{}".format(delete_data[need]),"")
            else:
                value = value.replace("<{}".format(delete_data[need]),"")
        need_delete_2 = value.split("[")    
        need=0
        delete_data_2 = []
        for need in range(len(need_delete_2)):
            if "]" in need_delete_2[need]:
                delete_data_2.append(need_delete_2[need].split("]")[0])
        delete_data_2.sort()
        if len(delete_data_2) > 0:
            need=0
            for need in range(len(delete_data_2)):
                value = value.replace("[{}]".format(delete_data_2[need]),"")               
        value = value.replace(">","\n",1).replace(">","").replace("&amp;","").replace("&nbsp;","").replace(":","").strip()
        return value

    titles = ["Type","Brand","Model Name","Official Price","Ports & Slots","Display","Processor",'Dimensions','Height(mm)','Depth(mm)','Width(mm)','Weight(kg)',"Graphics Card","Storage","Memory","Operating System","Audio and Speakers",'Power',"Web Link"]

    json_data = ['./data/hp/Desktops__product.json','./data/hp/workstation_Desktops_product.json']
    for i in range(len(json_data)):
        # 打开JSON文件
        with open(json_data[i], 'r', encoding='utf-8') as file:
            # 从文件中加载JSON数据
            data = json.load(file)   
        j = 0
        for D in data:
            Type, Brand, Model_Name, Official_Price, Dimensions,Weight, Ports,Power_Supply, Keyboard, PalmRest = "","Hp",D[2],D[1],"","","","","",""
            Slots, Ports_Slots, Camera, Display, Wireless, NFC, Primary_Battery, Processor, Graphics_Card = "","","","","","","","",""
            Storage, Memory, Operating_System, Audio_Speakers, User_guide, Web_Link = "","","","","",D[0]
            FPR_model,FPR,Display_cleck,Height,Depth,Width = "","","","","",""
            
            if "chrome" in Model_Name.lower():
                Type="Chrome"
            elif "workstation" in Model_Name.lower():
                Type="Workstation"
            elif "omen" in Model_Name.lower() or "victus" in Model_Name.lower():
                Type="Gaming"
            elif "thin client" in Model_Name.lower() or "pro" in Model_Name.lower() or "elite" in Model_Name.lower() or "t550" in Model_Name.lower():
                Type="Commercial" 
            elif "pavilion" in Model_Name.lower() or "envy" in Model_Name.lower():
                Type="Consumer"              
            else:
                Type="None Type_DT"
            
            D[3] = {key.strip(): value for key, value in D[3].items()}    
            lowercase_dict = {key.lower(): process_value(value) for key, value in D[3].items()}
            D[3] = lowercase_dict
            # if j ==1:
            #     print(list(D[3].keys()))
            
            if "processor" in D[3]:
                Processor = D[3]["processor"]        
            if "display" in D[3]:
                Display = D[3]["display"]        
            if "memory" in D[3]:
                Memory = D[3]["memory"]        
            if "operating system" in D[3]:
                Operating_System = D[3]["operating system"]    
            if "internal storage" in D[3]:
                Storage = D[3]["internal storage"]        
            if "audio features" in D[3]:
                Audio_Speakers = D[3]["audio features"]        
            if "graphics" in D[3]:
                Graphics_Card = D[3]["graphics"].split("&nbsp;")[-1].split("Integrated")[-1]        
            if "hard drive" in D[3]:
                Storage = D[3]["hard drive"]        
            if "storage" in D[3]:
                Storage = D[3]["storage"]
            if "wireless technology" in D[3]:
                Wireless = D[3]["wireless technology"]            
            if "external i/o ports" in D[3]:
                Ports = D[3]["external i/o ports"]        
            if "expansion slots" in D[3]:
                Slots = D[3]["expansion slots"]        
            if "dimensions (w x d x h)" in D[3]:
                Dimensions = D[3]["dimensions (w x d x h)"]        
            if "weight" in D[3]:
                Weight = D[3]["weight"]        
            if "memory" in D[3]:
                Memory = D[3]["memory"]       
            if "power supply" in D[3]:
                Power_Supply = D[3]["power supply"]
            if "chassis & power supply" in D[3]:
                Power_Supply = D[3]["chassis & power supply"]           
            if "processor and graphics" in D[3]:
                P_G = D[3]["processor and graphics"]
                Processor = P_G.split("+")[0].strip()
                Graphics_Card = P_G.split("+")[1].strip()
                
            Ports_Slots = Ports +"/n"+Slots
            if len(Model_Name.split(",")) > 1:
                orther = Model_Name.split(",")
                Model_Name = orther[0]
                num = 0
                if Storage == '':
                    Storage_data = 0
                else:
                    Storage_data = 1
                for num in range(len(orther)):
                    if "Windows" in orther[num]:
                        if Operating_System == '':
                            Operating_System = orther[num].strip()
                    elif "RAM" in orther[num]:
                        if Memory == '':
                            Memory = orther[num].strip()
                    elif "Intel®" in orther[num] or "Ryzen™" in orther[num]:
                        if Processor == '':
                            Processor = orther[num].strip()
                    elif "SSD" in orther[num] or "HDD" in orther[num]:
                        if Storage_data == 0:
                            Storage = Storage +"+"+ orther[num].strip()
            if len(Dimensions) > 5:
                N_D = Dimensions
                Dim = (N_D).split("x")
                W = float(Dim[0].strip())*25.4
                D = float(Dim[1].strip())*25.4
                H = float(Dim[2].split("in")[0].strip())*25.4
                Height = round(H,2)
                Depth = round(D,2)
                Width = round(W,2)
            if len(Weight) > 5:
                N_D = Weight
                Weight_kg = float(N_D.split("lb")[0].split("at")[-1].strip())*0.4536            
                Weight = round(Weight_kg,2)        
            
            if len(Model_Name.split("+"))>1:
                Ports_Slots = "Web No Data"
            
            if Graphics_Card == "" and Ports_Slots.strip() != "Web No Data":
                
                headers = {
                    'Origin': 'https://www.hp.com',
                    'Referer': 'https://www.hp.com/',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                        }
                response = requests.get(Web_Link, headers=headers)
                L_DT_soup = BeautifulSoup(response.text,'html.parser')
                L_DT_data = L_DT_soup.select("ul.ConfigurationsList-module_list__na0NO >li")
                k = 0
                for k in range(len(L_DT_data)):
                    L_DT_read_data = L_DT_data[k].text
                    L_DT_read_data = L_DT_read_data.split("+")
                    l = 0
                    for l in range(len(L_DT_read_data)):
                        if Graphics_Card == "":
                            if ("Intel" in L_DT_read_data[l] or "AMD" in L_DT_read_data[l]) and "Graphic" in L_DT_read_data[l]:
                                Graphics_Card = L_DT_read_data[l].split("Integrated")[-1]
                        if Processor =="":
                            if ("Intel" in L_DT_read_data[l] or "AMD" in L_DT_read_data[l]) and "Graphic" not in L_DT_read_data[l]:
                                Processor = L_DT_read_data[l]
                        if Memory == "":
                            if "RAM" in L_DT_read_data[l]:
                                Memory = L_DT_read_data[l]            
            j+=1    
            B = [Type, Brand, Model_Name, Official_Price, Ports_Slots.strip(), Display, Processor, Dimensions, Height, Depth, Width, Weight, Graphics_Card, Storage, Memory, Operating_System, Audio_Speakers,Power_Supply, Web_Link]
            A = pd.Series(titles)
            if i == 0 and j == 1:
                C = pd.DataFrame(B,index = A)
            else:
                B = pd.DataFrame(B,index = A)
                B.columns = [j-1]
                C = C.merge(B,how = "outer",left_index=True, right_index=True)    

    C = C.T
    C['Hard Drive'] = C['Storage']
    C['Power Supply'] = C['Power']
    C = C[["Type","Brand","Model Name","Official Price","Ports & Slots","Display","Processor","Graphics Card","Hard Drive","Memory","Operating System","Audio and Speakers","Height(mm)","Width(mm)","Depth(mm)","Weight(kg)",'Power Supply',"Web Link"]]
    C.to_csv("./data/hp/desktop.csv",encoding="utf-8-sig",index=False)
    
    

def data_to_excel_laptop():
    def process_value(value):
        if isinstance(value, list):
            v_num = 0
            v = ""
            for v_num in range(len(value)):
                v = v + '\n' +value[v_num]
            value = v
        else:
            value = value
        value = value.replace("</p></li><li><p>","\n")
        need_delete = value.split("<")    
        need=0
        delete_data = []
        for need in range(len(need_delete)):
            if ">" in need_delete[need]:
                delete_data.append(need_delete[need].split(">")[0])
        delete_data.sort()
        need=0
        for need in range(len(delete_data)):
            value = value.replace("<{}".format(delete_data[need]),"")
        need_delete_2 = value.split("[")    
        need=0
        delete_data_2 = []
        for need in range(len(need_delete_2)):
            if "]" in need_delete_2[need]:
                delete_data_2.append(need_delete_2[need].split("]")[0])
        delete_data_2.sort()
        if len(delete_data_2) > 0:
            need=0
            for need in range(len(delete_data_2)):
                value = value.replace("[{}]".format(delete_data_2[need]),"")                
        value = value.replace(">","\n",1).replace(">","").replace("&amp;","").replace("&nbsp;","").strip()
        return value

    titles = ["Type","Brand","Model Name","Official Price","Ports & Slots","Camera","Display","Primary Battery","Processor","Graphics Card","Storage","Memory","Operating System","Audio and Speakers",'Height(mm)','Depth(mm)','Width(mm)','Weight(kg)',"Wireless","NFC","FPR","FPR_model",'Power',"Web Link"]

    json_data = ['./data/hp/Laptops__product.json','./data/hp/workstation_Laptops_product.json']
    all_data = 0
    for i in range(len(json_data)):
        # 打开JSON文件
        with open(json_data[i], 'r', encoding='utf-8') as file:
            # 从文件中加载JSON数据
            data = json.load(file)
            all_data = all_data + len(data)
        j = 0
        for D in data:
            try:
                Type, Brand, Model_Name, Official_Price, Dimensions,Weight, Ports,Power_Supply, Keyboard, PalmRest = "","Hp",D[2],D[1],"","","","","",""
                Slots, Ports_Slots, Camera, Display, Wireless, NFC, Primary_Battery, Processor, Graphics_Card = "","","","","","No","","",""
                Storage, Memory, Operating_System, Audio_Speakers, User_guide, Web_Link = "","","","","",D[0]
                FPR_model,FPR,Display_cleck,Height,Depth,Width,WAN,PGM = "No","No","","","","","",""
                if "pen" not in Model_Name.lower():
                    if "chrome" in Model_Name.lower():
                        Type="Chrome"
                    elif "zbook" in Model_Name.lower() or "workstation" in Model_Name.lower():
                        Type="Workstation"
                    elif "omen" in Model_Name.lower() or "victus" in Model_Name.lower() or "gaming" in Model_Name.lower():
                        Type="Gaming" 
                    elif "dragonfly" in Model_Name.lower() or "pro" in Model_Name.lower() or "elite" in Model_Name.lower() or "fortis" in Model_Name.lower():
                        Type="Commercial"
                    elif "envy" in Model_Name.lower() or "pavilion" in Model_Name.lower():
                        Type="Consumer"      
                    else:
                        Type="None Type_NB"
                        
                    D[3] = {key.strip(): value for key, value in D[3].items()}    
                    lowercase_dict = {key.lower(): process_value(value) for key, value in D[3].items()}
                    D[3] = lowercase_dict
                    
                    G4,G5="",""
                    if len(D)>4:                
                        overview_specs = [D[4]["OVERVIEW"],D[4]["SPECS"]]
                        G1 = 0
                        for G in range(len(overview_specs)):
                            g = 0
                            for g in range(len(overview_specs[G])):
                                if "4G" in overview_specs[G][g] and G4 =="":                    
                                    G4 = "4G"
                                if "5G" in overview_specs[G][g] and G5 =="":
                                    G5 = "5G"
                        if G4 != "" and G5 != "":
                            WAN = "4G/5G"
                        elif G4 != "" and G5 == "":
                            WAN = "4G"
                        elif G4 == "" and G5 != "":
                            WAN = "5G"
                        else:
                            WAN = "No"
                
                    if "processor" in D[3]:
                        Processor = D[3]["processor"]        
                    if "display" in D[3]:
                        Display = D[3]["display"]        
                    if "memory" in D[3]:
                        Memory = D[3]["memory"]        
                    if "operating system" in D[3]:
                        Operating_System = D[3]["operating system"]    
                    if "internal storage" in D[3]:
                        Storage = D[3]["internal storage"]        
                    if "audio features" in D[3]:
                        Audio_Speakers = D[3]["audio features"]        
                    if "graphics" in D[3]:
                        Graphics_Card = D[3]["graphics"].split("Integrated")[-1]       
                    if "hard drive" in D[3]:
                        Storage = D[3]["hard drive"]        
                    if "internal drive" in D[3]:
                        Storage = D[3]["internal drive"]
                    if "storage" in D[3]:
                        Storage = D[3]["storage"]
                    if "internal m.2 storage" in D[3]:
                        Storage = D[3]["internal m.2 storage"]                        
                    if "wireless technology" in D[3]:
                        Wireless = D[3]["wireless technology"]            
                    if "external i/o ports" in D[3]:
                        Ports = D[3]["external i/o ports"]        
                    if "expansion slots" in D[3]:
                        Slots = D[3]["expansion slots"]                       
                    if "dimensions (w x d x h)" in D[3]:
                        Dimensions = D[3]["dimensions (w x d x h)"]        
                    if "weight" in D[3]:
                        Weight = D[3]["weight"]    
                    if "power supply" in D[3]:
                        Power_Supply = D[3]["power supply"]
                    if "ac adapter" in D[3]:
                        Power_Supply = D[3]["ac adapter"]
                    if "camera" in D[3]:
                        Camera = D[3]["camera"]
                    if "webcam" in D[3]:
                        Camera = D[3]["webcam"]
                    if "primary battery" in D[3]:
                        Primary_Battery = D[3]["primary battery"]
                    if "battery" in D[3]:
                        Primary_Battery = D[3]["battery"]
                    if "nfc" in D[3]:
                        if isinstance(D[3]["nfc"], list):
                            NFC = "Yes"
                        else:
                            NFC = "No"                
                    if "processor, graphics & memory" in D[3]:
                        PGM = D[3]["processor, graphics & memory"]
                        PGM_data = PGM.split("+")
                        Processor = PGM_data[0].strip()
                        Graphics_Card = PGM_data[1].split("Integrated")[-1].strip()
                        Memory = PGM_data[2].strip()
                            
                    if "processor, graphics, memory & hard disk" in D[3]:
                        PGM = D[3]["processor, graphics, memory & hard disk"]
                        PGM_data = PGM.split("+")
                        Processor = PGM_data[0].strip()
                        Graphics_Card = PGM_data[1].split("Integrated")[-1].strip()
                        Memory = PGM_data[2].strip()
                        Storage = PGM_data[3].strip()
                        
                    if "base features" in D[3]:
                        PGM = D[3]["base features"]
                        if "," in PGM:
                            PGM_data = PGM.split(",")
                        elif "+" in PGM:
                            PGM_data = PGM.split("+")
                        elif "and" in PGM:
                            PGM_data = PGM.split("and")
                        data_num = 0
                        for data_num in range(len(PGM_data)):
                            if ("Intel" in PGM_data[data_num] or "Ryzen"in PGM_data[data_num]) and "Graphics" not in PGM_data[data_num]:                        
                                Processor = PGM_data[data_num].split("and")[-1].strip()
                            if "RAM" in PGM_data[data_num] or "memory" in PGM_data[data_num]:
                                Memory = PGM_data[data_num].split("and")[-1].strip()
                            if "Graphic" in PGM_data[data_num]:
                                Graphics_Card = PGM_data[data_num].split("and")[-1].split("Integrated")[-1].strip()
                            if "storage" in PGM_data[data_num] or "eMMC" in PGM_data[data_num]:
                                Storage = PGM_data[data_num].split("and")[-1].strip()
                            if "camera" in PGM_data[data_num]:
                                Camera = PGM_data[data_num].split("and")[-1].strip()
            
                    if "finger print reader" in D[3]:
                        if "no" not in D[3]["finger print reader"] or "No" not in D[3]["finger print reader"]:
                            FPR = "Yes"
                            FPR_model = "Yes"
                        else:
                            FPR = "No"
                            FPR_model = "Yes"
                    if "processor and graphics" in D[3]:
                        P_G = D[3]["processor and graphics"]
                        Processor = P_G.split("+")[0].strip()
                        Graphics_Card = P_G.split("+")[1].split("Integrated")[-1].strip()
                    Ports_Slots = Ports +"\n"+Slots
                    Ports_Slots = Ports_Slots.strip()
                    
                    if len(Model_Name.split("+"))>1:
                        Ports_Slots = "Web No Data"
                        
                    if len(Model_Name.split(",")) > 1:
                        orther = Model_Name.split(",")
                        Model_Name = orther[0]
                        num = 0
                        if Storage == '':
                            Storage_data = 0
                        else:
                            Storage_data = 1
                        for num in range(len(orther)):
                            if "Windows" in orther[num]:
                                if Operating_System == '':
                                    Operating_System = orther[num].strip()
                            elif "RAM" in orther[num]:
                                if Memory == '':
                                    Memory = orther[num].strip()
                            elif "Intel" in orther[num] or "Ryzen" in orther[num]:
                                if Processor == '':
                                    Processor = orther[num].strip()
                            elif "SSD" in orther[num] or "HDD" in orther[num] or "storage" in orther[num]:
                                if Storage_data == 0:
                                    Storage = Storage +"+"+ orther[num].strip()
                    if len(Dimensions) > 5:
                        Dim = Dimensions.split("x")
                        W = float(Dim[0].split("at")[-1].strip())*25.4
                        De = float(Dim[1].strip())*25.4
                        H_real = Dim[2].split("in")[0].strip().split("-")
                        if len(H_real)>1:
                            h,H = 0,0
                            for h in range(len(H_real)):
                                if H < float(H_real[h].split("(")[0].strip()):
                                    H = float(H_real[h].split("(")[0].strip())
                                else:
                                    pass
                            H = H*25.4
                        else:
                            if len(Dim[2]) > 1:
                                H = float(Dim[2].split("in")[0].strip())*25.4
                            else:
                                H = float(Dim[3].split("in")[0].strip())*25.4
                        Height = round(H,2)
                        Depth = round(De,2)
                        Width = round(W,2)
                    if len(Weight) > 2:
                        N_D = Weight
                        Weight_kg_A = N_D.split("lb")[0].split("at")[-1].strip()
                        if "<" in Weight_kg_A:
                            Weight_kg_A = Weight_kg_A.split("<")[-1]
                            Weight_kg = float(Weight_kg_A)*0.4536            
                            Weight = "< {}".format(round(Weight_kg,2))
                        else:
                            Weight_kg = float(Weight_kg_A)*0.4536                      
                            Weight = round(Weight_kg,2)        
                    j+=1
                    B = [Type, Brand, Model_Name, Official_Price, Ports_Slots, Camera, Display, Primary_Battery, Processor, Graphics_Card, Storage, Memory, Operating_System, Audio_Speakers, Height, Depth, Width, Weight, Wireless, NFC, FPR, FPR_model,Power_Supply, Web_Link]
                    A = pd.Series(titles)
                    if i==0 and j == 1:
                        C = pd.DataFrame(B,index = A)
                    else:
                        B = pd.DataFrame(B,index = A)
                        B.columns = [j-1]
                        C = C.merge(B,how = "outer",left_index=True, right_index=True) 
            except:
                pass

    C =C.T
    C['Hard Drive'] = C['Storage']
    C['WWAN'] = C['Wireless']
    C['Power Supply'] = C['Power']
    C = C[["Type","Brand","Model Name","Official Price","Ports & Slots","Camera","Display","Primary Battery","Processor","Graphics Card","Hard Drive","Memory","Operating System","Audio and Speakers","Height(mm)","Width(mm)","Depth(mm)","Weight(kg)","WWAN","NFC","FPR_model","FPR",'Power Supply',"Web Link"]]
    C.to_csv("./data/hp/laptop.csv",encoding='utf-8-sig',index=False)
        




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