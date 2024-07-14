import json
import pandas as pd
titles = ["Type","Brand","Model Name","Official Price","Ports & Slots","Power Supply","Weight","Web Link"]
json_data = ['./data/lenovo/Docking_product.json']

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
    value = value.replace(">","\n",1).replace(">","").replace("&amp;","").replace("&nbsp;","").strip()
    return value

for i in range(len(json_data)):
    # 打开JSON文件
    with open(json_data[i], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
        data = json.load(file)
    j = 0
    for D in data:
        Type,Brand,Model_Name,Official_Price,Ports_Slots,Power_Supply,Weight,Web_Link="","Lenovo",D[0],D[2]["price"],"","","",D[1]       
        P1,P2,P3,P4,P5,P6="","","","","",""
        
        D[3] = {key.strip(): value for key, value in D[3].items()}
        lowercase_dict = {key.lower(): process_value(value) for key, value in D[3].items()}
        D[3] = lowercase_dict        
        
        if "audio ports" in D[3]:
            P1 = D[3]["audio ports"]            
        if "interfaces" in D[3]:
            P2 = D[3]["interfaces"]
        if "thunderbolt port" in D[3]:
            P3 = D[3]["thunderbolt port"]
        if "usb ports" in D[3]:
            P4 = D[3]["usb ports"]
        if "video ports" in D[3]:
            P5 = D[3]["video ports"]                	
        if "docking interface" in D[3]:
            P6 = D[3]["docking interface"]
        if "power provided" in D[3]:
            Power_Supply = D[3]["power provided"]
        if "weight" in D[3]:
            Weight = D[3]["weight"]               
        if "input power" in D[3]:
            Power_Supply = D[3]["input power"]     
               
        D[4] = {key.strip(): value for key, value in D[4].items()}
        lowercase_dict = {key.lower(): process_value(value) for key, value in D[4].items()}
        D[4] = lowercase_dict                
        if "audio ports" in D[4]:
            P1 = D[4]["audio ports"]        
        if "interfaces" in D[4]:
            P2 = D[4]["interfaces"]
        if "thunderbolt port" in D[4]:
            P4 = D[4]["thunderbolt port"]
        if "usb ports" in D[4]:
            P4 = D[4]["usb ports"]
        if "video ports" in D[4]:
            P5 = D[4]["video ports"]                	
        if "docking interface" in D[4]:
            P6 = D[4]["docking interface"]
        if "power provided" in D[4]:
            Power_Supply = D[4]["power provided"]
        if "weight" in D[4]:
            Weight = D[4]["weight"]
        if "input power" in D[4]:
            Power_Supply = D[4]["input power"]                  
        if "power" in D[4]:
            Power_Supply = D[4]["power"]
        if "features" in D[4]:
            Power_data = D[4]["features"].split(",")
            for AC in Power_data:
                if ("W" in AC and "Whr" not in AC) or "Adapter" in AC or "adapter" in AC:
                    Power_Supply = AC
                
        Ports_Slots = P1.strip()+"\n"+P2.strip()
        Ports_Slots = Ports_Slots.strip() +"\n" +P3.strip()
        Ports_Slots = Ports_Slots.strip() +"\n" +P4.strip()
        Ports_Slots = Ports_Slots.strip() +"\n" +P5.strip()
        Ports_Slots = Ports_Slots.strip() +"\n" +P6.strip()
        Ports_Slots = Ports_Slots.strip()
        
        if Weight != "":
            w = Weight.split("g")
            if "K" in w[0]:
                Weight = float(w[0].split("K")[0].split(":")[-1].strip())
            elif "k" in w[0]:
                Weight = float(w[0].split("k")[0].split(":")[-1].strip())
            elif "oz" in w[0]:
               Weight = round(float(w[0].split("oz")[0].strip())*0.0283495231,2)
            elif "lb" in w[0]:
                Weight = round(float(w[0].split("lb")[0].strip())*0.4536,2)
            else:
                Weight = round(float(w[0].strip())/1000,2)
                
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
C.to_csv("./data/lenovo/docking.csv",encoding="utf-8-sig",index=False)
