import glob


import torch
import pubchempy
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from torch_geometric.data import InMemoryDataset
import selfies as sf
class PubChemDataset(InMemoryDataset):
    def __init__(self, path):
        super(PubChemDataset, self).__init__()
        self.data, self.slices = torch.load(path)
    
    def __getitem__(self, idx):
        return self.get(idx)

# 加载数据集
data = PubChemDataset('/home/hukun/code/Tmm-llama/data/PubChem324kV2/PubChem324kV2/pretrain.pt')

# 函数：获取iUPAC名称，添加超时处理
def get_iupac_name(smiles, timeout=60):
    try:
        compounds = pubchempy.get_compounds(smiles, namespace='smiles', timeout=timeout)
        if compounds:
            return compounds[0].iupac_name
        return None
    except Exception as e:
        print(f"Error fetching IUPAC name for {smiles}: {e}")
        return None

# 并行获取iUPAC名称
def fetch_data_for_index(i):
    sample = data[i]
    smiles = sample["smiles"]
    cid = sample["cid"]
    text = sample["text"]
    # 获取 iupac name
    iupac_name = get_iupac_name(smiles)
    
    if iupac_name is not None:
        return [cid, smiles, text, iupac_name, None]  # 返回数据
    else:
        return [None, None, None, None, i]  # 返回失败的索引



def get_iupac_index_range(index_set:set):
    
    csv_file = f'./data/pubchem324k/pubchem_data_unfinished2.csv'
    df_columns = ["CID", "SMILES", "text", "iupac name"]
    df = pd.DataFrame(columns=df_columns)
    df.to_csv(csv_file, index=False)  # 写入表头

    # 准备存储数据的列表
    completed_indexes = set()  # 用于存储已经完成的索引
    unfinished_indexes = []  # 用于记录未完成的索引


    # 使用 ThreadPoolExecutor 来并行处理数据
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = []
        
        # 遍历数据集，为每个索引提交任务
        for i in sorted(index_set):
            futures.append(executor.submit(fetch_data_for_index, i))
        
        # 处理完成的任务
        for future in tqdm(as_completed(futures), desc="Processing", total=len(futures), unit="sample"):
            cid, smiles, text, iupac_name,failed_idx = future.result()
            
            if iupac_name is not None:
                # 保存有效数据
                temp_df = pd.DataFrame([[cid, smiles, text, iupac_name]], columns=df_columns)
                temp_df.to_csv(csv_file, mode='a', header=False, index=False)
                completed_indexes.add(failed_idx)  # 记录成功爬取的索引
            else:
                unfinished_indexes.append(failed_idx)  # 记录失败的索引

    # 保存未完成数据的索引到一个文件
    unfinished_file = f'./data/pubchem324k/unhandle_2.txt'
    with open(unfinished_file, 'w') as f:
        for idx in unfinished_indexes:
            f.write(f"{idx}\n")


    print("数据已成功保存为 CSV 文件！")
    print(f"未完成的数据索引已保存到 {unfinished_file}！")

def get_unfinished_set():
    # 定义文件名模式
    file_pattern = "./data/pubchem324k/unhandle_1.txt"

    # 初始化一个空集合
    combined_set = set()

    # 遍历所有匹配的文件
    for file_name in glob.glob(file_pattern):
        with open(file_name, 'r') as file:
            # 读取每一行并转换为整数，添加到集合中
            for line in file:
                try:
                    combined_set.add(int(line.strip()))
                except ValueError:
                    print(f"跳过非数字行: {line.strip()} (文件: {file_name})")

    # 打印合并后的集合
    print(len(combined_set))
    return combined_set


if __name__ == "__main__":
    index_set = get_unfinished_set()
    get_iupac_index_range(index_set)
    print("done")
