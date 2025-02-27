import json
import re

# 设置源文件路径和目标文件路径
start = 0
end = 260000
for i in range(start, end, 20000):

    source_file_path = f"/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation/m_d_g_{i}_{i+20000}.json"  # 替换为实际的源文件路径
    output_file_path = f"/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation/preprocessed_m_d_g_{i}_{i+20000}.txt"  # 替换为目标文件路径

    # 读取源文件

    with open(source_file_path, "r", encoding="utf-8") as file:
        raw_data = file.read()

    # 处理 output 字段中的换行符，合并多行内容为一行
    raw_data = re.sub(r'("output":\s*")([^"]*)(\n)([^"]*")', 
                        lambda m: m.group(1) + m.group(2).replace('\n', ' ') + m.group(4), 
                        raw_data, flags=re.DOTALL)
    # 替换反斜杠 `\` 为双反斜杠 `\\`
    raw_data = raw_data.replace('\\', '\\\\')
    def replace_quotes(text):
        if text:
            text_parts = text.split('"')
            if(len(text_parts) > 1):
                modified_text = re.sub(r'"', '\\"', text)
                text = modified_text
        return text

    # 正则表达式替换：只处理 output 和 iupac_name 之间的内容
    # def replacement_function(m):
    #     # 输出三部分
    #     print("Group 1 (before output content):", m.group(1))
    #     print("Group 2 (content of output):", m.group(2))
        
    #     # 返回替换后的文本
    #     return m.group(1) + replace_quotes(m.group(2)) 

    # # 正则表达式替换：只处理 output 和 iupac_name 之间的内容
    # raw_data = re.sub(r'("output":\s*")(.*?)(?=",\n\s*"iupac_name")', 
    #                     replacement_function, 
    #                     raw_data)

    raw_data = re.sub(r'("output":\s*")(.*?)(?=",\n\s*"iupac_name")', 
                        lambda m: m.group(1) + replace_quotes(m.group(2)), 
                        raw_data)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(raw_data)

    print(f"处理后的文本文件已保存为 {output_file_path}")

