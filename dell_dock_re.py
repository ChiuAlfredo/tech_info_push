import pandas as pd
import logging

# 配置日志
logging.basicConfig(filename='bug.log',
                    filemode='w',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    format='%(asctime)s %(filename)s %(levelname)s:%(message)s',
                    level=logging.INFO)

try:
    df2 = pd.read_excel("DELL_Dock.xlsx",index_col="Unnamed: 0")
    df2 = df2.T
    df2.reset_index(drop = True, inplace = True)
    
    Dock = df2["Weight"]
    
    #針對DELL重量進行處理 & 單位換算 & 資料切割
    j = 0
    for j in range(len(Dock)):
        if str(Dock[j]) != "nan":
            if "g" in str(Dock[j]):
                D_kg = str(Dock[j])
                D_kg = D_kg.split("g")[0].split("(")[-1].strip()
                df2["Weight"][j] = round(float(D_kg)/1000,2)
            elif "oz" in str(Dock[j]):
                D_kg = str(Dock[j])
                D_kg = D_kg.split("oz")[0].split("(")[-1].strip()
                df2["Weight"][j] = round(float(D_kg)*0.0283495231,2)
            elif "lbs" in str(Dock[j]):
                D_kg = str(Dock[j])
                D_kg = D_kg.split("lbs")[0].split("(")[-1].strip()
                df2["Weight"][j] = round(float(D_kg)*0.453,2)
    
    #重新排序<依商品名稱>   
    df2 = df2.sort_values(["Model Name"],ascending=True)
    
    df2["Type"] = ""
    df2 = df2.rename(columns={'USB-C': 'Ports & Slots'})
    df2 = df2[["Type","Brand","Model Name","Official Price","Ports & Slots","Power Supply","Weight","Web Link"]]
    
    df2 = df2.rename(columns={'Weight': 'Weight(kg)'})
    df2 = df2.T
        
    df2.to_excel("DELL_Dock.xlsx")
    
except Exception as bug:
    # 捕获并记录错误日志
    logging.error(f"An error occurred: {str(bug)}", exc_info=True)
