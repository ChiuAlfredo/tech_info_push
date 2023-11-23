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

for i in range(len(json_data)):
    # 打开JSON文件
    with open(json_data[i], 'r', encoding='utf-8') as file:
        # 从文件中加载JSON数据
        data = json.load(file)
    j = 0
    for D in data:
        Type, Brand, Model_Name, Official_Price, Dimensions,Weight, Ports,Power_Supply, Keyboard, PalmRest = "","Hp",D[2],D[1],"","","","","",""
        Slots, Ports_Slots, Camera, Display, Wireless, NFC, Primary_Battery, Processor, Graphics_Card = "","","","","","No","","",""
        Storage, Memory, Operating_System, Audio_Speakers, User_guide, Web_Link = "","","","","",D[0]
        FPR_model,FPR,Display_cleck,Height,Depth,Width,WAN,PGM = "No","No","","","","","",""
        if "chrome" in Model_Name.lower():
            Type="Chrome"
        elif "dragonFly pro" in Model_Name.lower() or "envy" in Model_Name.lower() or "pavilion" in Model_Name.lower():
            Type="Consumer"
        elif "dragonFly" in Model_Name.lower() or "pro" in Model_Name.lower() or "elite" in Model_Name.lower() or "fortis" in Model_Name.lower():
            Type="Commercial"
        elif "omen" in Model_Name.lower() or "victus" in Model_Name.lower():
            Type="Gaming"
        elif "zbook" in Model_Name.lower() or "workstation" in Model_Name.lower():
            Type="Workstation"       
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
            Camera = D[3]["camera"].split("Integrated")[-1]
        if "webcam" in D[3]:
            Camera = D[3]["webcam"].split("Integrated")[-1]
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
                    Camera = PGM_data[data_num].split("and")[-1].split("Integrated")[-1].strip()
  
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
                H = float(Dim[2].split("in")[0].strip())*25.4
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
            
    C.to_excel("HP_NB.xlsx")
    
