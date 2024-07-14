import pandas as pd 
import datetime

keyword_list = ['laptop','desktop','docking']

company_list = ['Dell','hp','lenovo']

def get_monday():
    today = datetime.date.today()
    weekday = today.weekday()
    if today.weekday() == 0:
        return today
    else:
        days_until_next_monday = (7 - weekday) % 7 or 7
        next_monday = today + datetime.timedelta(days=days_until_next_monday)
        return next_monday

day = get_monday()
output_path = f'./data/output/Competitors_Data_{day.year}{day.month:02d}{day.day:02d}.xlsx'
output_convert_path = f'./data/output/Competitors_Data_Convert-{day.year}{day.month:02d}{day.day:02d}.xlsx'

with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer, \
    pd.ExcelWriter(output_convert_path, engine='openpyxl', mode='w') as writer_convert:
    for keyword in keyword_list:
        # keyword = keyword_list[2]
        keyword_df = pd.DataFrame()
        for company in company_list:
            # company = company_list[1]
            company_df = pd.read_csv(f'./data/{company}/{keyword}.csv')
            keyword_df = pd.concat([keyword_df, company_df], ignore_index=True)
            
        # 将 keyword_df 写入对应的工作表
        keyword_df.to_excel(writer, sheet_name=keyword, index=False)
        # 转置后的 keyword_df 写入另一个文件的对应工作表
        keyword_df.transpose().to_excel(writer_convert, sheet_name=keyword, index=False)
