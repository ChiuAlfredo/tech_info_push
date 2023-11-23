import json
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
        
        if "pavilion" in Model_Name.lower() or "envy" in Model_Name.lower():
            Type="Consumer"
        elif "thin client" in Model_Name.lower() or "pro" in Model_Name.lower() or "elite" in Model_Name.lower():
            Type="Commercial"
        elif "omen" in Model_Name.lower() or "victus" in Model_Name.lower():
            Type="Gaming"
        elif "workstation" in Model_Name.lower():
            Type="Workstation"       
        else:
            Type="None Type"
        
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
            
C.to_excel("HP_DT.xlsx")

