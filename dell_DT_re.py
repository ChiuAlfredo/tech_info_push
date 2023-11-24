import pandas as pd
import logging

# 配置日志
logging.basicConfig(filename='bug.log',
                    filemode='w',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    format='%(asctime)s %(filename)s %(levelname)s:%(message)s',
                    level=logging.INFO)

try:
    my_header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    
    #desktop資料重整
    df1 = pd.read_excel("DELL_DT.xlsx",index_col=0)
    df1 = df1.T
    df1 = df1.sort_values(["Model Name"],ascending=True)
    df1.reset_index(drop = True, inplace = True)
    df1.rename(columns={'Power': 'Power Supply'}, inplace=True)
    df1.rename(columns={'Storage': 'Hard Drive'}, inplace=True)
    
    #將商品名稱與長寬深/重量抓出建立字典<方便後續補齊 減少需抓捕資料>
    Dell_DT_data = {}
    DNB = 0
    for DNB in range(len(df1["Brand"])):
        if df1["Model Name"][DNB] not in Dell_DT_data and len(str(df1["Dimensions and Weight"][DNB])) > 25 :
            Dell_DT_data[df1["Model Name"][DNB]] = str(df1["Dimensions and Weight"][DNB])
            
    Height = []
    Width = []
    Depth = []
    Weight = []
    
    #檢查DELL_DT缺值
    #尚不需
    
    #針對DELL重量體積資料處理 & 單位換算 & 資料切割
    S_W = df1["Dimensions and Weight"]
    for i in range(len(S_W)):
        if str(Dell_DT_data.get(df1["Model Name"][i])) != "None":
            A00 = Dell_DT_data[df1["Model Name"][i]].lower()
            A0 = A00.split("weight")
            no_weight = 0
            for no_weight in range(len(A0)):
                height_data = " "
                width_data = " "
                depth_data = " "
                Weight_data = " "
                if "weight" not in A0[no_weight].lower() and "kg" not in A0[no_weight].lower() and ("mm" in A0[no_weight].lower() or "cm" in A0[no_weight].lower()):
                    A1_text = A0[no_weight].split("width")
                    A1_besa = A0[no_weight]                   
                if len(A1_text) <= 2:
                    if "mm" in A1_besa:
                        A1 = A1_besa.split("mm")
                        mm_data = 0
                        for mm_data in range(len(A1)):
                            if "height" in A1[mm_data]:
                                height_data = A1[mm_data].split("height")[-1].split("3. ")[0].split("2. ")[0].split("(")[-1].split("-")[-1].split("–")[-1].split(":")[-1].strip()
                            elif "width" in A1[mm_data]:
                                width_data = A1[mm_data].split("width")[-1].split("3. ")[0].split("2. ")[-1].split("(")[-1].split(":")[-1].strip()
                            elif "depth" in A1[mm_data] or "length" in A1[mm_data]:
                                depth_data = A1[mm_data].split("depth")[-1].split("length")[-1].split("3. ")[-1].split("(")[-1].split(":")[-1].strip()
                    elif "cm" in A1_besa:
                        A1 = A1_besa.split("cm")
                        cm_data = 0
                        for cm_data in range(len(A1)):
                            if "height" in A1[cm_data]:
                                height_data = float(A1[cm_data].split("height")[-1].split("3. ")[0].split("2. ")[0].split("(")[-1].split(")")[0].split("-")[-1].split(":")[-1].strip())*10
                            elif "width" in A1[cm_data]:
                                width_data = float(A1[cm_data].split("width")[-1].split("3. ")[0].split("2. ")[-1].split("(")[-1].split(":")[-1].strip())*10
                            elif "depth" in A1[cm_data] or "length" in A1[cm_data]:
                                depth_data = float(A1[cm_data].split("depth")[-1].split("length")[-1].split("3. ")[-1].split("(")[-1].split(":")[-1].strip())*10
                if len(A0) >1:               
                    if len(df1["Model Name"][i].split("Special")) > 1:
                        if "kg" in A0[-2]:
                            A2 = A0[-2].split("kg")
                            Weight_data = A2[0].split("(")[-1].split(":")[-1].strip()
                        elif "g" in A0[-2]:
                            A2 = A0[-2].split("g")
                            Weight_data = float(A2[0].split("(")[-1].split(":")[-1].strip())/1000
                    else:
                        data_real_set = 0
                        for data_real_set in range(len(A0)):
                            if "g)" in A0[data_real_set] or "kg)" in A0[data_real_set]:
                                A_date = A0[data_real_set]
                                if "kg" in A_date:
                                    A2 = A_date.split("kg")
                                    Weight_data = A2[0].split("(")[-1].split(":")[-1].strip()
                                elif "g" in A_date:
                                    A2 = A_date.split("g")
                                    Weight_data = float(A2[0].split("(")[-1].split(":")[-1].strip())/1000
                                
            else:
                pass
            Weight.append(Weight_data)
            Height.append(height_data)
            Width.append(width_data)
            Depth.append(depth_data)
        else:
            Height.append("")        
            Width.append("")
            Depth.append("")
            Weight.append("")
          
    #重新填充資料欄位與去除欄位
    df1["Height"] = Height
    df1["Width"] = Width
    df1["Depth"] = Depth
    df1["Weight"] = Weight
    df1 = df1.drop(columns='Dimensions and Weight')
    
    #Type分類
    Type = []
    re_type_DT = 0
    AA = df1["Brand"]
    for re_type_DT in range(len(df1["Model Name"])):
        #Dell分類
        if df1.iloc[re_type_DT]["Brand"] == "Dell":
            if "precision" in df1.iloc[re_type_DT]["Model Name"].lower() or "workstation" in df1.iloc[re_type_DT]["Model Name"].lower():
                Type.append("Workstation") 
            elif "alienware" in df1.iloc[re_type_DT]["Model Name"].lower():
                Type.append("Gaming")
            elif "optiplex" in df1.iloc[re_type_DT]["Model Name"].lower() or "vostro" in df1.iloc[re_type_DT]["Model Name"].lower():
                Type.append("Commercial") 
            elif "inspiron" in df1.iloc[re_type_DT]["Model Name"].lower() or "xps" in df1.iloc[re_type_DT]["Model Name"].lower():
                Type.append("Consumer")                    
            else:
                Type.append("None Type")    
     
    df1["Type"] = Type    
    #排序
    df1 = df1[["Type","Brand","Model Name","Official Price","Ports & Slots","Display","Processor","Graphics Card","Hard Drive","Memory","Operating System","Audio and Speakers","Height","Width","Depth","Weight",'Power Supply',"Web Link"]]
    df1 = df1.rename(columns={'Height': 'Height(mm)','Width': 'Width(mm)','Depth': 'Depth(mm)','Weight': 'Weight(kg)'})
    df1 = df1.T
    #儲存資料
    df1.to_excel("DELL_DT.xlsx") 
    
except Exception as bug:
    # 捕获并记录错误日志
    logging.error(f"An error occurred: {str(bug)}", exc_info=True)
