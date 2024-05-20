import json
import pandas as pd

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
            
C.to_excel("HP_Dock.xlsx")
