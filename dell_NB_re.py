import pandas as pd
import logging
import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# 配置日志
logging.basicConfig(filename='bug.log',
                    filemode='w',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    format='%(asctime)s %(filename)s %(levelname)s:%(message)s',
                    level=logging.INFO)

try:
    df = pd.read_excel("DELL_NB.xlsx",index_col=0)
    
    df = df.T
    df = df.sort_values(["Model Name"],ascending=True)
    df.reset_index(drop = True, inplace = True)
    df.rename(columns={'Power': 'Power Supply'}, inplace=True)
    df.rename(columns={'Storage': 'Hard Drive'}, inplace=True)
    my_header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    
    #將商品名稱與長寬深/重量抓出建立字典<方便後續補齊 減少需抓捕資料>
    Dell_NB_data_DW = {}
    Dell_NB_data_camera = {}
    DNB = 0
    for DNB in range(len(df["Brand"])):
        if df["Model Name"][DNB] not in Dell_NB_data_DW and len(str(df["Dimensions and Weight"][DNB])) > 25 :
            Dell_NB_data_DW[df["Model Name"][DNB]] = str(df["Dimensions and Weight"][DNB])        
        if df["Model Name"][DNB] not in Dell_NB_data_camera and len(str(df["Camera"][DNB])) > 10 :
            Dell_NB_data_camera[df["Model Name"][DNB]] = str(df["Camera"][DNB])  
    
    DNB = 0
    for DNB in range(len(df["Brand"])):
        if len(str(df["Camera"][DNB])) < 10 and df["Model Name"][DNB] in Dell_NB_data_camera:
            df["Camera"][DNB] = Dell_NB_data_camera.get(df["Model Name"][DNB])
    
    Height = []
    Width = []
    Depth = []
    Weight = []
 
    #Dell_NB 資料檢驗/補充
    DNB = 0
    for DNB in range(len(df["Brand"])):        
        if len(str(df["Ports & Slots"][DNB])) < 20:
            print(DNB)
            delay = random.uniform(0.5, 5.0)
            sleep(delay)
            url_dell = df["Web Link"][DNB] + "#techspecs_section"
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            dell_dock = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
            dell_dock.get(url_dell)
            sleep(2)
            dell_dock.execute_script("document.body.style.zoom='50%'")
            sleep(2)
            dell_dock.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5);")
            sleep(2)
            soup = BeautifulSoup(dell_dock.page_source,"html.parser")
            dell_dock.quit()
            one_data = soup.select("ul.cf-hero-bts-list > li")
            Ports_Slots=""
            for one in one_data:
                two_data = one.select("p")
                if "Power Supply" in two_data[0].text:
                    Power_Supply = two_data[0].text.strip()
                if "Ports" in two_data[0].text or "Slots" in two_data[0].text or "PORTS" in two_data[0].text:
                    two_data = one.select(" p > a")
                    Ports_Slots = two_data[0]["data-description"]
                    Ports_Slots = Ports_Slots.replace("<br>","\n")
                    Ports_Slots = Ports_Slots.replace("<ul>","")
                    Ports_Slots = Ports_Slots.replace("</ul>","")
                    Ports_Slots = Ports_Slots.replace("<li>"," ")
                    Ports_Slots = Ports_Slots.replace("</li>","\n")
                    Ports_Slots = Ports_Slots.replace("<span>"," ")
                    Ports_Slots = Ports_Slots.replace("</span>","")
            No_select_data = soup.select("li.mb-2")
            for no_data in No_select_data:
                No_select_title = no_data.select("div")
                No_select_Data = no_data.select("p")
                if "Ports" in No_select_title[0].text or "Slots" in No_select_title[0].text or "PORTS" in No_select_title[0].text:
                    Ports_Slots = Ports_Slots + "\n" + No_select_Data[0].text
            df["Ports & Slots"][DNB] = Ports_Slots
    #針對DELL重量體積資料處理 & 單位換算 & 資料切割        
    S_W = df["Dimensions and Weight"]
    i = 0
    for i in range(len(S_W)):
        if str(Dell_NB_data_DW.get(df["Model Name"][i])) != "None":
            A00 = Dell_NB_data_DW[df["Model Name"][i]].lower()
            A0 = A00.split("weight")
            no_weight = 0
            for no_weight in range(len(A0)):
                height_data = " "
                width_data = " "
                depth_data = " "
                if "weight" not in A0[no_weight].lower() and "kg" not in A0[no_weight].lower() and ("mm" in A0[no_weight].lower() or "cm" in A0[no_weight].lower()):
                    A1_text = A0[no_weight].split("width")
                    A1_besa = A0[no_weight]                   
                if len(A1_text) <= 2:
                    if "mm" in A1_besa:
                        if "h/w/d" in A1_besa:
                            A1_hwd = A1_besa.split("(")
                            hwd = 0
                            for hwd in range(len(A1_hwd)):
                                if "mm" in A1_hwd[hwd]:
                                    A1_new_besa = A1_hwd[hwd]
                                    A1 = A1_new_besa.split("x")
                                    height_data = A1[0].split("height")[-1].split("3. ")[0].split("2. ")[0].split("(")[-1].split("-")[-1].split("–")[-1].split(":")[-1].split("mm")[0].strip()
                                    width_data = A1[1].split("width")[-1].split("3. ")[0].split("2. ")[-1].split("(")[-1].split(":")[-1].split("mm")[0].strip()
                                    depth_data = A1[2].split("depth")[-1].split("length")[-1].split("3. ")[-1].split("(")[-1].split(":")[-1].split("mm")[0].strip()
                        else:            
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
                Weight_data = " "
                if len(A0) >1:
                    if len(df["Model Name"][i].split("Special")) > 1:
                        if "kg" in A0[-2]:
                            A2 = A0[-2].split("kg")
                            Weight_data = A2[0].split("(")[-1].split(":")[-1].strip()
                        elif "g" in A0[-2]:
                            A2 = A0[-2].split("g")
                            Weight_data = float(A2[0].split("(")[-1].split(":")[-1].strip())/1000
                    else:
                        if "kg" in A0[-1]:
                            A2 = A0[-1].split("kg")
                            Weight_data = A2[0].split("(")[-1].split(":")[-1].strip()
                        elif "g" in A0[-1]:
                            A2 = A0[-1].split("g")
                            Weight_data = float(A2[0].split("(")[-1].split(":")[-1].strip())/1000                
            else:
                pass
            Height.append(height_data)
            Width.append(width_data)
            Depth.append(depth_data)
            Weight.append(Weight_data)
        else:
            Height.append(" ")        
            Width.append(" ")
            Depth.append(" ")
            Weight.append(" ")
    
    #重新填充資料欄位與去除欄位
    df["Height"] = Height
    df["Width"] = Width
    df["Depth"] = Depth
    df["Weight"] = Weight
    
    #Type分類
    Type_NB = []
    re_type_NB = 0
    for re_type_NB in range(len(df["Model Name"])):
        #Dell分類
        if df.iloc[re_type_NB]["Brand"] == "Dell":
            if "chrome" in df.iloc[re_type_NB]["Model Name"].lower():
                Type_NB.append("Chrome")
                df.iloc[re_type_NB]["Operating System"] = "Chrome OS"
            elif "alienware" in df.iloc[re_type_NB]["Model Name"].lower():
                Type_NB.append("Gaming")
            elif "g series" in df.iloc[re_type_NB]["Model Name"].lower():
                Type_NB.append("Consumer/Gaming")
            elif "inspiron" in df.iloc[re_type_NB]["Model Name"].lower() or "xps" in df.iloc[re_type_NB]["Model Name"].lower():
                Type_NB.append("Consumer")
            elif "latitude" in df.iloc[re_type_NB]["Model Name"].lower() or "vostro" in df.iloc[re_type_NB]["Model Name"].lower():
                Type_NB.append("Commercial")       
            elif "precision" in df.iloc[re_type_NB]["Model Name"].lower():
                Type_NB.append("Workstation")
            elif "gaming"in df.iloc[re_type_NB]["Model Name"].lower():
                Type_NB.append("Consumer/Gaming")
            else:
                Type_NB.append("None Type_NB")
    
    df["Type"] = Type_NB    
    #排序
    df = df[["Type","Brand","Model Name","Official Price","Ports & Slots","Camera","Display","Primary Battery","Processor","Graphics Card","Hard Drive","Memory","Operating System","Audio and Speakers","Height","Width","Depth","Weight","Wireless","NFC","FPR_model","FPR",'Power Supply',"Web Link"]]
    df.rename(columns={'Wireless': 'WWAN'}, inplace=True)
    df.rename(columns={'Storage': 'Hard Drive'}, inplace=True)
    df = df.rename(columns={'Height': 'Height(mm)','Width': 'Width(mm)','Depth': 'Depth(mm)','Weight': 'Weight(kg)'})
    df = df.T   
    # #儲存資料
    df.to_excel("DELL_NB.xlsx")
    
except Exception as bug:
    # 捕获并记录错误日志
    logging.error(f"An error occurred: {str(bug)}", exc_info=True)
