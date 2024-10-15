import pandas as pd
import json
import os
# 映射状态更新
mapping_df = pd.read_excel('风机点表.xlsx')

point_mapping = pd.Series(mapping_df['测点标签'].values, index=mapping_df['scada变量名']).to_dict()

print(os.getcwd())

with open('point_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(point_mapping, f, ensure_ascii=False, indent=4)