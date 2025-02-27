import torch
import pubchempy
import pandas as pd
import time
from torch_geometric.data import InMemoryDataset
import selfies as sf
from tqdm import tqdm


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

# 准备存储数据的列表
data_list = []
unfinished_indexes = []  # 用于记录未完成的索引

# 打开一个 CSV 文件以便实时保存
csv_file = './data/pubchem324k/pubchem_data.csv'
df_columns = ["CID", "SMILES", "text", "iupac name","SELFIES"]
df = pd.DataFrame(columns=df_columns)
df.to_csv(csv_file, index=False)  # 写入表头

# 遍历数据集
for i in tqdm(range(len(data)), desc="Processing", unit="sample"):
    sample = data[i]
    smiles = sample["smiles"]
    cid = sample["cid"]
    text = sample["text"]
    
    # 获取 iupac name
    iupac_name = get_iupac_name(smiles)
    selfies_ = sf.encoder(smiles)
    if iupac_name is not None:
        # 保存有效数据
        data_list.append([cid, smiles, text, iupac_name,selfies_])
        # 实时保存到 CSV 文件
        temp_df = pd.DataFrame([[cid, smiles, text, iupac_name,selfies_]], columns=df_columns)
        temp_df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        # 记录未完成的索引
        unfinished_indexes.append(i)


# 保存未完成数据的索引到一个文件
unfinished_file = './data/pubchem324k/unfinished_indexes.txt'
with open(unfinished_file, 'w') as f:
    for idx in unfinished_indexes:
        f.write(f"{idx}\n")

print("数据已成功保存为 CSV 文件！")
print(f"未完成的数据索引已保存到 {unfinished_file}！")
