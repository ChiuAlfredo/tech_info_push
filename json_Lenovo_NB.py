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
    value = value.replace(">","\n",1).replace(">","").replace("&amp;","").replace("&nbsp;","").strip()
    return value

titles = ["Type","Brand","Model Name","Official Price","Ports & Slots","Camera","Display","Primary Battery","Processor","Graphics Card","Storage","Memory","Operating System","Audio and Speakers",'Height(mm)','Depth(mm)','Width(mm)','Weight(kg)',"Wireless","NFC","FPR","FPR_model",'Power',"Web Link"]

json_data = ['./data/lenovo/Laptops_product.json']
for i in range(len(json_data)):
    # 打开JSON文件
    with open(json_data[i], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
            data = json.load(file)
    j = 0
    for D in data:
        Type, Brand, Model_Name, Official_Price, Dimensions,Weight, Ports,Power_Supply, Keyboard, PalmRest = "","Lenovo",D[0],D[2]["price"],"","","","","",""
        Slots, Ports_Slots, Camera, Display, Wireless, NFC, Primary_Battery, Processor, Graphics_Card = "","","","","","No","","",""
        Storage, Memory, Operating_System, Audio_Speakers, User_guide, Web_Link = "","","","","",D[1]
        FPR_model,FPR,Display_cleck,Height,Depth,Width,WAN = "No","No","","","","","No"

        if "Workstation" in Model_Name.lower():
            Type = "Workstation"
        elif "ideaPad" in Model_Name.lower() or "slim" in Model_Name.lower() or "yoga" in Model_Name.lower():
            Type="Consumer"
        elif "legion" in Model_Name.lower() or "loq" in Model_Name.lower():
            Type="Gaming"
        elif "thinkbook" in Model_Name.lower() or "thinkpad" in Model_Name.lower():
            Type="Commercial"         
        else:
            Type="None Type_NB"
                  
        if i == 1:
            Type="workstation"
   
        D[3] = {key.strip(): value for key, value in D[3].items()}
        lowercase_dict = {key.lower(): process_value(value) for key, value in D[3].items()}
        D[3] = lowercase_dict
        
        if "wwan" in D[3]:
            WAN_data = D[3]["wwan"]
            if "4G" in WAN_data and "5G" in WAN_data:
                WAN = "4G/5G"
            elif "4G" in WAN_data and "5G" not in WAN_data:
                WAN = "4G"
            elif "4G" not in WAN_data and "5G" in WAN_data:
                WAN = "5G"
            else:
                WAN = "No"
        Wireless = WAN
            
        if "processor" in D[3]:
            Processor = D[3]["processor"]        
        if "display" in D[3]:
            Display = D[3]["display"]        
        if "memory" in D[3]:
            Memory = D[3]["memory"]        
        if "operating system" in D[3]:
            Operating_System = D[3]["operating system"]
        if "graphics" in D[3]:
            Graphics_Card = D[3]["graphics"]
        if "graphic card" in D[3]:
            Graphics_Card = D[3]["graphic card"]                   
        if "audio" in D[3]:
            Audio_Speakers = D[3]["audio"] 
        if "battery" in D[3]:
            Primary_Battery = D[3]["battery"]
        if "storage" in D[3]:
            Storage = D[3]["storage"]
                      
        if "finger print reader" in D[3]:
            if "no" not in D[3]["finger print reader"]:
                FPR = "Yes"
                FPR_model = "Yes"
            else:
                FPR = "No"
                FPR_model = "Yes"
        
        D[4] = {key.strip(): value for key, value in D[4].items()}
        lowercase_dict = {key.lower(): process_value(value) for key, value in D[4].items()}
        D[4] = lowercase_dict
        if "finger print reader" in D[4]:
            if "no" not in D[4]["finger print reader"]:
                FPR = "Yes"
                FPR_model = "Yes"
            else:
                FPR = "No"
                FPR_model = "Yes"
        if "what’s in the box" in D[4]:
            power_data = D[4]["what’s in the box"]                
            need_delete = power_data.split("<")
            need=0
            delete_data = []
            for need in range(len(need_delete)):
                if ("W" in need_delete[need] and "Whr" not in need_delete[need]) or "Adapter" in need_delete[need] or "adapter" in need_delete[need]:
                    PS_data = need_delete[need].split("\n")
                    for AC in PS_data:
                        if ("W" in AC and "Whr" not in AC) or "Adapter" in AC or "adapter" in AC:
                            Power_Supply = AC
                                
        if "what's in the box" in D[4]:
            power_data = D[4]["what's in the box"]                
            need_delete = power_data.split("\n")
            need=0
            delete_data = []
            for need in range(len(need_delete)):
                if ("W" in need_delete[need] and "Whr" not in need_delete[need]) or "Adapter" in need_delete[need] or "adapter" in need_delete[need]:
                    PS_data = need_delete[need].split("\n")
                    for AC in PS_data:
                        if ("W" in AC and "Whr" not in AC) or "Adapter" in AC or "adapter" in AC:
                            Power_Supply = AC
        if "more information" in D[4]:        
            power_data = D[4]["more information"]                
            need_delete = power_data.split("\n")
            need=0
            delete_data = []
            for need in range(len(need_delete)):
                if ("W" in need_delete[need] and "Whr" not in need_delete[need]) or "Adapter" in need_delete[need] or "adapter" in need_delete[need]:
                    PS_data = need_delete[need].split("\n")
                    for AC in PS_data:
                        if ("W" in AC and "Whr" not in AC) or "Adapter" in AC or "adapter" in AC:
                            Power_Supply = AC
        if "more information1" in D[4]:        
            power_data = D[4]["more information1"]                
            need_delete = power_data.split("\n")
            need=0
            delete_data = []
            for need in range(len(need_delete)):
                if ("W" in need_delete[need] and "Whr" not in need_delete[need]) or "Adapter" in need_delete[need] or "adapter" in need_delete[need]:
                    PS_data = need_delete[need].split("\n")
                    for AC in PS_data:
                        if ("W" in AC and "Whr" not in AC) or "Adapter" in AC or "adapter" in AC:
                            Power_Supply = AC                                                    
        if "audio" in D[4]:
            Audio_Speakers = D[4]["audio"]             

        if "battery" in D[4]:
            Primary_Battery = D[4]["battery"].replace('style=white-space: normal;',"")
        if "battery life" in D[4]:
            Primary_Battery = D[4]["battery life"].replace('*',"\n")
        if "camera" in D[4]:
            Camera = D[4]["camera"]
        if "weight" in D[4]:
            Weight = D[4]["weight"]
        if "dimensions (h x w x d)" in D[4]:
            Dimensions = D[4]["dimensions (h x w x d)"].split(":")[-1]
        if "ports" in D[4]:
            Ports = D[4]["ports"]        
        if "slots" in D[4]:
            Slots = D[4]["slots"]
        if "ports/slots" in D[4]:
            PS = D[4]["ports/slots"]
        elif "Ports/Slots" in D[4]:
            PS = D[4]["Ports/Slots"]
            
        print(D[4])
                    
        if len(Ports) > 10 and len(Slots) > 10:        
            Ports_Slots = Ports +"\n"+Slots
            Ports_Slots = Ports_Slots.strip()
        elif len(PS) > 10: 
            Ports_Slots = PS.strip()
        
        if len(Model_Name.split("+"))>1:
            Ports_Slots = "Web No Data"
                        
        if len(Dimensions) > 5:
            Dim = Dimensions.split("/")
            D_cut = 0
            for D_cut in range(len(Dim)):
                if len(Dim[D_cut].split("mm")) > 2:
                    Dim_1 = Dim[D_cut].split("mm")
                    if len(Dim_1[2]) < 2:
                        Dim_1 = Dim[D_cut].split("x")
                        H = Dim_1[0].split(":")[-1].split("-")[-1].split("at")[-1].split("~")[-1].split("covers")[-1].split("chassis")[-1].split("as")[-1].split("–")[-1].split("aluminum")[-1].split("mm")[0].split("from")[-1].split(";")[-1].split(">")[-1].strip()
                        W = Dim_1[1].split("mm")[0].split(";")[-1].split(">")[-1].strip()
                        De = Dim_1[2].split("as")[-1].split("-")[-1].split("–")[-1].split("~")[-1].split("mm")[0].split(";")[-1].split(">")[-1].strip()
                    else:
                        H = Dim_1[0].split("x")[-1].split(":")[-1].split("-")[-1].split("at")[-1].split("~")[-1].split("covers")[-1].split("chassis")[-1].split("as")[-1].split("–")[-1].split("aluminum")[-1].split("mm")[0].split("from")[-1].split(";")[-1].split(">")[-1].strip()
                        W = Dim_1[1].split("x")[-1].split("mm")[0].split(";")[-1].split(">")[-1].strip()
                        De = Dim_1[2].split("x")[-1].split("as")[-1].split("-")[-1].split("–")[-1].split("~")[-1].split("mm")[0].split(";")[-1].split(">")[-1].strip()
                elif "mm" in Dim[D_cut] and "inches" in Dim[D_cut]:
                    Dim = D.split("(")
                    hwd = 0
                    for hwd in range(len(Dim)):
                        if "mm" in Dim[hwd]:
                            H = Dim[hwd].split(":")[-1].split("x")[0].split("from")[-1].split(";")[-1].split(">")[-1].strip()
                            W = Dim[hwd].split(":")[-1].split("x")[1].split(";")[-1].split(">")[-1].strip()
                            De = Dim[hwd].split(":")[-1].split("x")[2].split("as")[-1].split("mm")[0].split(";")[-1].split(">")[-1].strip()
                elif "mm" in Dim[D_cut] and (len(Dim[D_cut].split("mm")[0]) > len(Dim[D_cut].split("mm")[1])):
                        H = Dim[D_cut].split("(mm")[0].split("x")[0].split("from")[-1].split(";")[-1].split(">")[-1].strip()
                        W = Dim[D_cut].split("(mm")[0].split("x")[1].split(";")[-1].split(">")[-1].strip()
                        De = Dim[D_cut].split("(mm")[0].split("x")[2].split("mm")[0].split(";")[-1].split(">")[-1].strip()
        Height = round(float(H),2)
        Depth = round(float(De),2)
        Width = round(float(W),2)
            
        if len(Weight) > 2:
            W_cut = Weight.split("at")[-1].split("from")[-1].split("than")[-1].split("Starting")[-1].split("weight")[-1].split("g")
            if len(W_cut) > 1:
                if str(W_cut[0])[-1] == "K" or str(W_cut[-2])[-1] == "k":
                    if "<" in W_cut[0]: 
                        Wei = W_cut[0].split("K")[0].split("k")[0].split("/")[-1].split("(")[-1].split("<")[-1].split(":")[-1].split(";")[-1]
                        Wei = float(Wei)
                        symbol = "<"
                    elif "Up" in W_cut[0]:
                        Wei = W_cut[0].split("K")[0].split("k")[0].split("/")[-1].split("(")[-1].split("to")[-1].split(":")[-1].split(";")[-1]
                        Wei = float(Wei)
                        symbol = ">"
                    else:
                        Wei = W_cut[0].split("K")[0].split("k")[0].split("/")[-1].split("(")[-1].split("<")[-1].split(":")[-1].split(";")[-1]
                        Wei = float(Wei)
                else:
                    if "<" in W_cut[0]: 
                        Wei = W_cut[0].split("/")[-1].split("(")[-1].split("<")[-1].split(":")[-1].split(";")[-1]
                        Wei = round(float(Wei)/1000,2)
                        symbol = "<"
                    else:
                        Wei = W_cut[0].split("/")[-1].split("(")[-1].split("<")[-1].split(":")[-1].split(";")[-1]
                        Wei = round(float(Wei)/1000,2)
            else:
                Wei = ""
        Weight = Wei
        
        j+=1
        B = [Type, Brand, Model_Name, Official_Price, Ports_Slots, Camera, Display, Primary_Battery, Processor, Graphics_Card, Storage, Memory, Operating_System, Audio_Speakers, Height, Depth, Width, Weight, Wireless, NFC, FPR, FPR_model,Power_Supply, Web_Link]
        A = pd.Series(titles)
        if i==0 and j == 1:
            C = pd.DataFrame(B,index = A)
        else:
            B = pd.DataFrame(B,index = A)
            B.columns = [j-1]
            C = C.merge(B,how = "outer",left_index=True, right_index=True)    
            
    C.to_excel("Lenovo_NB.xlsx")
