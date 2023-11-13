import json
import pandas as pd
need_data = ["Processor"]

# 打开JSON文件
with open('workstation_Desktops_product.json', 'r', encoding='utf-8') as file:
    # 从文件中加载JSON数据
    data = json.load(file)
# 现在，变量"data"包含了从JSON文件中读取的数据
print(len(data))

for n in data:
    print(n)
# df = pd.DataFrame([data[3]])
