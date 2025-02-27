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

# 读取已经保存的 CSV 文件，获取已经爬取的 CID
def get_existing_cids(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return set(df['CID'].dropna().astype(str))  # 返回已爬取数据的CID集合
    except FileNotFoundError:
        return set()  # 如果没有文件，则返回空集合

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
    selfies_ = sf.encoder(smiles)
    # 获取 iupac name
    iupac_name = get_iupac_name(smiles)
    
    if iupac_name is not None:
        return [cid, smiles, text, iupac_name,selfies_, None]  # 返回数据
    else:
        return None  # 返回失败数据

# 打开一个 CSV 文件以便实时保存
csv_file = './data/pubchem324k/pubchem_data_2.csv'
df_columns = ["CID", "SMILES", "text", "iupac name","SELFIES"]

# 获取已经爬取过的 CID
existing_cids = get_existing_cids(csv_file)

# 使用 ThreadPoolExecutor 来并行处理数据
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    
    # 遍历数据集，为每个未爬取过的 CID 提交任务
    for i in range(0,len(data)):
        sample = data[i]
        cid = sample["cid"]
        if str(cid) not in existing_cids:
            futures.append(executor.submit(fetch_data_for_index, i))
    
    # 处理完成的任务
    for future in tqdm(as_completed(futures), desc="Processing", total=len(futures), unit="sample"):
        result = future.result()
        
        if result:
            cid, smiles, text, iupac_name, selfies_ = result
            # 保存有效数据
            temp_df = pd.DataFrame([[cid, smiles, text, iupac_name, selfies_]], columns=df_columns)
            temp_df.to_csv(csv_file, mode='a', header=False, index=False)

print("数据已成功保存为 CSV 文件！")

