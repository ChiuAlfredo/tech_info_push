import pandas as pd
import xlsxwriter
import logging
import random
from time import sleep
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# 配置日志
logging.basicConfig(filename='bug.log',
                    filemode='w',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    format='%(asctime)s %(filename)s %(levelname)s:%(message)s',
                    level=logging.INFO)

#laptop資料重整
df = pd.read_excel("DELL_NB.xlsx",index_col=0)
df = df.T
df.reset_index(drop = True, inplace = True)

my_header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

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
        
df = df.T

#載入其他公司資料進行合併

df_1 = pd.read_excel("HP_NB.xlsx",index_col="Unnamed: 0")
df_2 = pd.read_excel("Lenovo_NB.xlsx",index_col="Unnamed: 0")
df_1 = df_1.T
df_2 = df_2.T
df_1.rename(columns={'Storage': 'Hard Drive'}, inplace=True)
df_2.rename(columns={'Storage': 'Hard Drive'}, inplace=True)
df_1.reset_index(drop = True, inplace = True)
df_2.reset_index(drop = True, inplace = True)
             
df_1 = df_1.T   
df_2 = df_2.T
df = df.merge(df_1,how = "outer", left_index=True, right_index=True)
df = df.merge(df_2,how = "outer", left_index=True, right_index=True)

#desktop資料重整
df1 = pd.read_excel("DELL_DT.xlsx",index_col=0)
df1 = df1.T
df1.reset_index(drop = True, inplace = True)
#Dell_DT 資料檢驗/補充
DNB = 0
for DNB in range(len(df1["Brand"])):        
    if df1["Weight(kg)"][DNB] ==" ":
        print(DNB)
        delay = random.uniform(0.5, 5.0)
        sleep(delay)
        url_dell = df1["Web Link"][DNB] + "#techspecs_section"
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
        Href = soup.select("div.pd-feature-wrap")
        dell_dock.quit()
        href_number = 0
        max_kg,kg = 0,0
        if len(Href) > 1:
            for href in Href:            
                dell_tatle = href.select("h2")
                if len(dell_tatle) > 0:
                    if "weight" in dell_tatle[0].text.lower():
                        dell_tatle_data = href.select("div > div.pd-item-desc")
                        data_number = 0
                        for data_number in range(len(dell_tatle_data)):
                            if "weight" in dell_tatle_data[data_number].text.lower() or "kg" in dell_tatle_data[data_number].text.lower():
                                data_kg = dell_tatle_data[data_number].text.lower()
                                data_kg = data_kg.split(":")
                                data_kg_number = 0
                                for data_kg_number in range(len(data_kg)):
                                    if "kg" in data_kg[data_kg_number]:
                                        kg = data_kg[data_kg_number].split("kg")[0].split("(")[-1]
                                        if max_kg < float(kg):
                                            max_kg = float(kg)
        df1["Weight(kg)"][DNB] = max_kg
df1 = df1.T
#載入其他公司資料進行合併
df1_1 = pd.read_excel("HP_DT.xlsx",index_col="Unnamed: 0")    
df1_2 = pd.read_excel("Lenovo_DT.xlsx",index_col="Unnamed: 0")
df1_1 = df1_1.T
df1_2 = df1_2.T
df1_1.rename(columns={'Storage': 'Hard Drive'}, inplace=True)
df1_2.rename(columns={'Storage': 'Hard Drive'}, inplace=True)
df1_1.reset_index(drop = True, inplace = True)
df1_2.reset_index(drop = True, inplace = True)

# 檢查HP_DT
re_load = 0
for re_load in range(len(df1_1)):
    if str(df1_1['Ports & Slots'][re_load]) != "Web No Data":
        if str(df1_1['Processor'][re_load]) == "Nan" and str(df1_1['Graphics Card'][re_load]) == "Nan" and str(df1_1['Memory'][re_load]) == "Nan":
            print(re_load)
            Processor = "Nan"
            GC = "Nan"
            Memory = "Nan"
            data_url = df1_1['Web Link'][re_load]
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            HP_DT_data = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
            HP_DT_data.get(data_url)
            sleep(2)
            L_DT_soup = BeautifulSoup(HP_DT_data.page_source,'html.parser')
            L_DT_data_n = L_DT_soup.select("li.Typography-module_root__eQwd4.Typography-module_bodyS__DBLtm.Typography-module_responsive__iddT7")
            L_DT_data_n_date = L_DT_data_n[1].text
            L_DT_data_n_date = L_DT_data_n_date.split("+")
            df1_1['Processor'][re_load] = L_DT_data_n_date[0]
            df1_1['Graphics Card'][re_load] = L_DT_data_n_date[1]
            df1_1['Memory'][re_load] = L_DT_data_n_date[2]
                    
        if str(df1_1['Official Price'][re_load]) == "Nan":
            print(re_load)
            Price = "Nan"
            data_url = df1_1['Web Link'][re_load]
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            HP_DT_data = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
            HP_DT_data.get(data_url)
            sleep(2)
            L_DT_soup = BeautifulSoup(HP_DT_data.page_source,'html.parser')
            L_DT_data_n = L_DT_soup.select("div.Typography-module_root__eQwd4.Typography-module_boldL__LZR-5.PriceBlock-module_hasActiveDeal__W4zIr.Typography-module_responsive__iddT7")
            if len(L_DT_data_n) <1:
                L_DT_data_n = L_DT_soup.select("div.Typography-module_root__eQwd4.Typography-module_boldL__LZR-5.Typography-module_responsive__iddT7")
            HP_DT_data.quit()
            if len(L_DT_data_n) >0:           
                Price = L_DT_data_n[0].text
                Price = Price.replace("$","")
            df1_1['Official Price'][re_load] = Price
        if str(df1_1['Height(mm)'][re_load]) == "nan" or str(df1_1['Processor'][re_load]) == "Nan" or str(df1_1['Graphics Card'][re_load]) == "Nan":
            print(re_load)
            data_url = df1_1['Web Link'][re_load]
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            HP_DT_data = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
            HP_DT_data.get(data_url)
            sleep(2)
            L_DT_soup = BeautifulSoup(HP_DT_data.page_source,'html.parser')
            L_DT_data_n = L_DT_soup.select("div.Spec-module_spec__71K6S > div.Spec-module_innerLeft__Z13zG > p")
            L_DT_data_d_ack = L_DT_soup.select("div.Spec-module_spec__71K6S > div.Spec-module_innerRight__4TTuE")
            L_DT_specs = L_DT_soup.select("div.Container-module_root__luUPH.Container-module_container__jSUGk > div.Footnotes-module_item__LOUR3 > div")
            HP_DT_data.quit()
            specs_data = []
            W,D,H,Weight_kg = "No_Data","No_Data","No_Data","No_Data"
            if len(L_DT_specs) > 0:
                L_DT_specs_list = L_DT_specs[-1].select("span")        
                if len(L_DT_specs_list) >0:
                    for specs in L_DT_specs_list:
                        specs_data.append(specs.text)
            j=0            
            for j in range(len(L_DT_data_n)):
                L_DT_data_d = L_DT_data_d_ack[j].select("div.Spec-module_valueWrapper__DTxWC > p.Typography-module_root__eQwd4.Typography-module_bodyM__XNddq.Spec-module_value__9FkNI.Typography-module_responsive__iddT7 > span")
                #抓取特徵內容
                N_D = L_DT_data_d[0].text
                if "[" in N_D and "]" in N_D:
                    N_Dnum = N_D.split("[")[-1].split("]")[0]
                    num = 0
                    for num in range(len(N_Dnum.split(','))):
                        sp_num = 0
                        for sp_num in range(len(specs_data)):
                            if N_Dnum.split(',')[num] in specs_data[sp_num]:
                                N_D = N_D.replace(N_Dnum.split(',')[num], specs_data[sp_num].split("]")[-1])             
                if L_DT_data_n[j].text =="Dimensions (W X D X H)":
                    Dim = (N_D).split("x")
                    W = round(float(Dim[0].strip())*25.4,2)
                    D = round(float(Dim[1].strip())*25.4,2)
                    H = round(float(Dim[2].split("in")[0].strip())*25.4,2)
                elif L_DT_data_n[j].text =="Weight":
                    Weight_kg = round(float(N_D.split("lb")[0].strip())*0.4536,2)            
            df1_1['Height(mm)'][re_load] = H
            df1_1['Depth(mm)'][re_load] = D
            df1_1['Width(mm)'][re_load] = W
            df1_1['Weight(kg)'][re_load] = Weight_kg

df1_1 = df1_1.T
df1_2 = df1_2.T
df1 = df1.merge(df1_1,how = "outer", left_index=True, right_index=True)
df1 = df1.merge(df1_2,how = "outer", left_index=True, right_index=True)    

#docking資料重整
df2 = pd.read_excel("DELL_Dock.xlsx",index_col="Unnamed: 0")

#載入其他公司資料進行合併
df2_1 = pd.read_excel("HP_Dock.xlsx",index_col="Unnamed: 0")
df2_2 = pd.read_excel("Lenovo_docking.xlsx",index_col="Unnamed: 0")
df2 = df2.merge(df2_1,how = "outer", left_index=True, right_index=True)
df2 = df2.merge(df2_2,how = "outer", left_index=True, right_index=True)
    
#分別對合併完的資料特徵進行重新排序
df = df.T
    
#排序
df = df[["Type","Brand","Model Name","Official Price","Ports & Slots","Camera","Display","Primary Battery","Processor","Graphics Card","Hard Drive","Memory","Operating System","Audio and Speakers","Height(mm)","Width(mm)","Depth(mm)","Weight(kg)","WWAN","NFC","FPR_model","FPR",'Power Supply',"Web Link"]]

df1 = df1.T      
#排序
df1 = df1[["Type","Brand","Model Name","Official Price","Ports & Slots","Display","Processor","Graphics Card","Hard Drive","Memory","Operating System","Audio and Speakers","Height(mm)","Width(mm)","Depth(mm)","Weight(kg)",'Power Supply',"Web Link"]]

df2 = df2.T
df2 = df2[["Type","Brand","Model Name","Official Price","Ports & Slots","Power Supply","Weight(kg)","Web Link"]]

df = df.T.fillna('NA')
df1 = df1.T.fillna('NA')
df2 = df2.T.fillna('NA')
    
# #儲存資料
writer = pd.ExcelWriter('Data_products_total.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='laptop', index=True,header = False)
df1.to_excel(writer, sheet_name='desktop', index=True,header = False)
df2.to_excel(writer, sheet_name='docking', index=True,header = False)
writer.save()

