import json
import pandas as pd


titles = ["Type","Brand","Model Name","Official Price","Ports & Slots","Display","Processor",'Dimensions','Height(mm)','Depth(mm)','Width(mm)','Weight(kg)',"Graphics Card","Storage","Memory","Operating System","Audio and Speakers",'Power',"Web Link"]

json_data = ['./data/lenovo/Desktops_product.json','./data/lenovo/thinkstation_product.json']

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
        # print(j)
        Type, Brand, Model_Name, Official_Price, Dimensions,Weight, Ports,Power_Supply, Keyboard, PalmRest = "","Lenovo",D[0],D[2]["price"],"","","","","",""
        Slots, Ports_Slots, Camera, Display, Wireless, NFC, Primary_Battery, Processor, Graphics_Card = "","","","","","","","",""
        Storage, Memory, Operating_System, Audio_Speakers, User_guide, Web_Link = "","","","","",D[1]
        FPR_model,FPR,Display_cleck,Height,Depth,Width,PS = "","","","","","",""
        H,W,De = "","",""
        
        if "workstation" in Model_Name.lower() or "thinkstation" in Model_Name.lower():
            Type = "Workstation"
        elif "thinkbook" in Model_Name.lower() or "thinkpad" in Model_Name.lower() or "thinkcentre" in Model_Name.lower() or "ideacentre" in Model_Name.lower():
            Type = "Commercial"  
        elif "legion" in Model_Name.lower() or "loq" in Model_Name.lower():
            Type = "Gaming"
        elif "yoga" in Model_Name.lower():
            Type = "Consumer" 
        else:
            Type = "None Type_DT"
        
        D[3] = {key.strip(): value for key, value in D[3].items()}    
        lowercase_dict = {key.lower(): process_value(value) for key, value in D[3].items()}
        D[3] = lowercase_dict
        
        if "processor" in D[3]:
            Processor = D[3]["processor"]         
        if "graphic card" in D[3]:
            Graphics_Card = D[3]["graphic card"].split("Integrated")[-1]  
        if "memory" in D[3]:
            Memory = D[3]["memory"]  
        if "operating system" in D[3]:
            Operating_System = D[3]["operating system"]  
        if "storage" in D[3]:
            Storage = D[3]["storage"]    
                
        D[4] = {key.strip(): value for key, value in D[4].items()}
        lowercase_dict = {key.lower(): process_value(value) for key, value in D[4].items()}
        D[4] = lowercase_dict
        if "memory" in D[4] and "memory" not in D[3]:
            Memory = D[4]["memory"] 
        if "power" in D[4]:
            Power_Supply = D[4]["power"]
        if "ac adapter" in D[4]:
            Power_Supply = D[4]["ac adapter"]   
        if "power supply" in D[4]:
            Power_Supply = D[4]["power supply"]                
        if "power supply unit (psu)" in D[4]:
            Power_Supply = D[4]["power supply unit (psu)"]
        if "psu" in D[4]:
            Power_Supply = D[4]["psu"]
        if "power supply unit" in D[4]:
            Power_Supply = D[4]["power supply unit"]
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
        if "audio" in D[4]:
            Audio_Speakers = D[4]["audio"]                
        if "display" in D[4]:
            Display = D[4]["display"]              
            Display = Display.replace("&quot;","").strip()
        if "weight" in D[4]:
            Weight = D[4]["weight"]
        if "net weight" in D[4]:
            Weight = D[4]["net weight"]
        if "starting weight" in D[4]:
            Weight = D[4]["starting weight"]
        if "dimension (w x d x h)" in D[4]:
            Dimensions = D[4]["dimension (w x d x h)"]
        if "dimension (d x w x h)" in D[4]:
            Dimensions = D[4]["dimension (d x w x h)"]
        if "dimension (w x h x d)" in D[4]:
            Dimensions = D[4]["dimension (w x h x d)"]
        if "dimension (d x h x w)" in D[4]:
            Dimensions = D[4]["dimension (d x h x w)"]
        if "dimension (h x w x d)" in D[4]:
            Dimensions = D[4]["dimension (h x w x d)"] 
        if "dimensions (w x d x h)" in D[4]:
            Dimensions = D[4]["dimensions (w x d x h)"]
        if "dimensions (d x w x h)" in D[4]:
            Dimensions = D[4]["dimensions (d x w x h)"]
        if "dimensions (w x h x d)" in D[4]:
            Dimensions = D[4]["dimensions (w x h x d)"]
        if "dimensions (d x h x w)" in D[4]:
            Dimensions = D[4]["dimensions (d x h x w)"]
        if "dimensions (h x w x d)" in D[4]:
            Dimensions = D[4]["dimensions (h x w x d)"]              
        if "dimensions" in D[4]:
            Dimensions = D[4]["dimensions"]

        if "ports/slots" in D[4]:
            PS = D[4]["ports/slots"]
        if "ports / slots" in D[4]:
            PS = D[4]["ports / slots"]
        if "ports" in D[4]:
            PS = D[4]["ports"]
        if "slots" in D[4]:
            PS = D[4]["slots"]
            
        F_P,R_P,S_P = "","",""
        if "fornt ports" in D[4]:
            PS = D[4]["fornt ports"]
        if "rear ports" in D[4]:
            PS = D[4]["rear ports"]
        if "side ports" in D[4]:
            PS = D[4]["side ports"] 
        if F_P != "" or R_P != "" or S_P != "":
            Ports_Slots = F_P +"\n"+ R_P
            Ports_Slots = Ports_Slots.strip() +"\n"+ S_P
                    
        if len(Ports) > 10 and len(Slots) > 10:        
            Ports_Slots = Ports +"\n"+Slots
            Ports_Slots = Ports_Slots.strip()
        elif len(PS) > 10: 
            Ports_Slots = PS.strip()
        Ports_Slots = Ports_Slots.replace('style="white-space: normal;"', '')
        N11b,N12b,N13b,N11,N12,N13 = 0,0,0,0,0,0
        if len(Dimensions) > 5:
            Dimensions = Dimensions.replace("&quot;", "")
            Dimensions_1 = Dimensions.split("\n")
            D_number = 0
            for D_number in range(len(Dimensions_1)):
                reD1 = Dimensions_1[D_number].lower().split("/")
                reD = 0
                for reD in range(len(reD1)):
                    if "mm" in reD1[reD]:
                        N1 = reD1[reD].split(":")
                        N1 = N1[-1].split("x")
                        N11 = N1[0].split("mm")[0].split("at")[-1].split("from")[-1].split("(")[0].strip()
                        N12 = N1[1].split("mm")[0].split("at")[-1].split("from")[-1].split("(")[0].strip()
                        N13 = N1[2].split("mm")[0].split("at")[-1].split("from")[-1].split("(")[0].strip()
                    if float(N11) > N11b:
                        N11b = float(N11)
                    if float(N12) > N11b:
                        N12b = float(N12)
                    if float(N13) > N11b:
                        N13b = float(N13)
                    
            if "dimensions (w x h x d)" in D[4] or "dimension (w x h x d)" in D[4]:
                Dimensions_data = "{}x{}x{}".format(N12,N11,N13)
            elif "dimensions (d x h x w)" in D[4] or "dimension (d x h x w)" in D[4]:
                Dimensions_data = "{}x{}x{}".format(N12,N13,N11)
            elif "dimensions (w x d x h)" in D[4] or "dimension (w x d x h)" in D[4]:
                Dimensions_data = "{}x{}x{}".format(N13,N11,N12)
            elif "dimensions (d x w x h)" in D[4] or "dimension (d x w x h)" in D[4]:
                Dimensions_data = "{}x{}x{}".format(N13,N12,N11)
            else:
                Dimensions_data = "{}x{}x{}".format(N11,N12,N13)
            Dimensions = Dimensions_data.replace("&nbsp;", "")
            
            H = Dimensions.split("x")[0].split("(")[0].split("thin as ")[-1].split("-")[-1].split("(")[0].split("–")[-1].split("aluminum")[-1].split("chassis")[-1].split("covers")[-1]
            W = Dimensions.split("x")[1].split("thin as ")[-1].split("-")[-1].split("(")[0].split("–")[-1].split("aluminum")[-1].split("chassis")[-1].split("covers")[-1]
            De = Dimensions.split("x")[2].split("thin as ")[-1].split("-")[-1].split("(")[0].split("–")[-1].split("aluminum")[-1].split("chassis")[-1].split("covers")[-1]
            Height = round(float(H),2)
            Depth = round(float(De),2)
            Width = round(float(W),2)
        
        Weight_big,weight_data = 0,0
        if len(Weight) > 5:
            weight_data_1 = Weight
            weight_data_2 = weight_data_1.split("\n")
            weight_data_number = 0
            for weight_data_number in range(len(weight_data_2)):
                if "kg" in weight_data_2[weight_data_number]:
                    weight_data = weight_data_2[weight_data_number].replace('Starting', ' ').split("kg")[0].split("(")[-1].split("at")[-1].split("rom")[-1].split("/")[-1].split(":")[-1].split("Arounweight_data")[-1].split("to")[-1].split("Around")[-1].strip()
                    weight_data = float(weight_data)
                elif "Kg" in weight_data_2[weight_data_number]:
                    weight_data = weight_data_2[weight_data_number].replace('Starting', ' ').split("Kg")[0].split("(")[-1].split("at")[-1].split("rom")[-1].split("/")[-1].split(":")[-1].split("Arounweight_data")[-1].split("to")[-1].split("Around")[-1].strip()
                    weight_data = float(weight_data)
                elif "g" in weight_data_2[weight_data_number]:
                    weight_data = weight_data_2[weight_data_number].replace('Starting', ' ').split("g")[0].split("(")[-1].split("at")[-1].split("rom")[-1].split("/")[-1].split(":")[-1].split("Arounweight_data")[-1].split("to")[-1].split("Around")[-1].strip()
                    weight_data = round(float(weight_data)/1000,2) 
                if weight_data > Weight_big:
                    Weight_big = weight_data              
            Weight = Weight_big   
        
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
C.to_csv("./data/lenovo/desktop.csv",encoding="utf-8-sig",index=False)

