import pandas as pd
import glob

# 定义文件名模式
file_pattern = "./data/pubchem324k/pubchem_data_*.csv"

# 初始化一个空列表，用于存储每个文件的 DataFrame
dataframes = []

# 遍历所有匹配的文件
for file_name in glob.glob(file_pattern):
    # 读取 CSV 文件
    print(file_name)
    # df = pd.read_csv(file_name)
    # 将 DataFrame 添加到列表中
    # dataframes.append(df)

# 合并所有 DataFrame
# combined_df = pd.concat(dataframes, ignore_index=True)

# # 保存合并后的 DataFrame 到一个新的 CSV 文件
# combined_df.to_csv("combined_pubchem_data.csv", index=False)

# print("合并完成！合并后的文件已保存为 combined_pubchem_data.csv")