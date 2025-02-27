import json
import os
import re

# 设置目录路径，假设所有json文件都在一个文件夹中
directory = '/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation/'  # 替换为实际文件夹路径

# 创建一个空列表用于存储所有数据
merged_data = []

# 定义命名规则的正则表达式
file_pattern = re.compile(r"test_m_d_g_\d+_\d+\.json")

# 遍历目录中的所有文件
for filename in sorted(os.listdir(directory)):
    if file_pattern.match(filename):  # 只处理符合命名规则的文件
        # 拼接文件路径
        file_path = os.path.join(directory, filename)
        print(file_path)        
        # 读取JSON文件
        with open(file_path, "r") as file:
            raw_data = file.read()


        # 解析 JSON 数据
        data = json.loads(raw_data)

            # 为每条数据加上一个 "id" 字段
        for idx, entry in enumerate(data):
            entry["id"] = len(merged_data) + idx  # 确保 id 唯一且连续
        merged_data.extend(data)

# 保存合并后的数据到一个新的 JSON 文件
with open("/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation/test_data.json", "w") as output_file:
    # 写入开头的 "[" 符号，开始一个 JSON 数组
    output_file.write("[\n")
    
    # 写入合并的数据，每条数据之间添加换行符
    for idx, entry in enumerate(merged_data):
        # 为了格式化，每个字段换行
        json.dump(entry, output_file, indent=4)
        if idx < len(merged_data) - 1:
            output_file.write(",\n")  # 除了最后一项外，每条数据后加逗号
        else:
            output_file.write("\n")  # 最后一项不加逗号
    
    # 写入结尾的 "]" 符号，结束 JSON 数组
    output_file.write("]")

print("所有符合条件的文件已合并并保存为")
