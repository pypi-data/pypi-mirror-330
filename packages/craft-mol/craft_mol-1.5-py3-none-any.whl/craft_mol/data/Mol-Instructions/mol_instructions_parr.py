import json
import pubchempy
import selfies as sf
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import os

# 加载自定义数据集，区分 train 和 test 数据
def load_custom_dataset(json_file_path):
    """加载自定义数据集，区分 train 和 test 数据"""
    train_data = []
    test_data = []

    # 读取 JSON 文件
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 遍历数据，按照 'split' 将数据分配到 train 或 test
    for item in data:
        split = item["metadata"].get("split", "train")  # 默认是 'train'
        if split == "train":
            train_data.append(item)
        elif split == "test":
            test_data.append(item)
        else:
            # 如果有其他的 split 类型，可以根据需要处理
            print(f"Unknown split: {split}")

    return train_data, test_data


# 提取数据中的SELFIES并转换为SMILES
def extract_smiles_from_selfies(selfies_tokens):
    return sf.decoder(selfies_tokens)


# 函数：获取IUPAC名称，添加超时处理
def get_iupac_name(smiles, timeout=60):
    try:
        compounds = pubchempy.get_compounds(smiles, namespace='smiles', timeout=timeout)
        if compounds:
            return compounds[0].iupac_name
        return None
    except Exception as e:
        print(f"Error fetching IUPAC name for {smiles}: {e}")
        return None


# 并行获取IUPAC名称
def fetch_data_for_index(i, dataset):
    sample = dataset[i]
    selfies_tokens = sample["input"]  # 获取SELFIES
    smiles = extract_smiles_from_selfies(selfies_tokens) if selfies_tokens else None  # 转换SELFIES为SMILES
    # 使用索引作为CID
    cid = i
    
    # 获取IUPAC名称
    if smiles:
        iupac_name = get_iupac_name(smiles)
        if iupac_name:
            return {"cid": cid, "smiles": smiles, "iupac_name": iupac_name, "instruction": sample["instruction"], "output": sample["output"], "metadata": sample["metadata"]}
        else:
            return {"cid": cid, "smiles": smiles, "iupac_name": None, "instruction": sample["instruction"], "output": sample["output"], "metadata": sample["metadata"]}
    return {"cid": cid, "smiles": None, "iupac_name": None, "instruction": sample["instruction"], "output": sample["output"], "metadata": sample["metadata"]}


def save_to_json_file(results, output_file, file_exists):
    """将结果保存到 JSON 文件中"""
    if file_exists:
        # 如果文件存在，先读取已有的数据
        with open(output_file, 'r+', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_data.extend(results)  # 合并新数据和已有数据
            f.seek(0)  # 回到文件开头
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
    else:
        # 如果文件是空的，创建一个新的文件并写入数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"定时保存了 {len(results)} 条数据到文件")

# 批量爬取IUPAC名称并保存为新的JSON文件
def get_iupac_index_range(start_index, length, dataset, max_len, output_file, failed_indexes_file):
    save_interval=100
    if start_index + length > max_len:
        length = max_len - start_index
    
    # 准备存储数据的列表
    results = []
    failed_indexes = []
    file_exists = False
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))  # 如果文件夹不存在则创建文件夹
    # 使用ThreadPoolExecutor并行获取IUPAC名称
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = []

        # 提交任务
        for i in range(start_index, start_index + length):
            futures.append(executor.submit(fetch_data_for_index, i, dataset))

        # 处理完成的任务
        for i, future in enumerate(tqdm(as_completed(futures), desc="Processing", total=len(futures), unit="sample")):
            result = future.result()
            if result["iupac_name"] is None:
                failed_indexes.append(result["cid"])
            else:
                results.append({
                    "instruction": result["instruction"],
                    "input": result["smiles"],
                    "iupac_name": result["iupac_name"] if result["iupac_name"] else "null",
                    "output": result["output"],
                    "metadata": result["metadata"]
                })
            if (i + 1) % save_interval == 0 or (i + 1) == len(futures):  # 在每 `save_interval` 个任务后保存
                save_to_json_file(results, output_file, file_exists)
                file_exists = True 

    with open(failed_indexes_file, 'a', encoding='utf-8') as f:
        for failed_idx in failed_indexes:
            f.write(f"{failed_idx}\n")

    print(f"数据已成功保存为 JSON 文件：{output_file}")
    print(f"爬取失败的分子索引已保存到 {failed_indexes_file}！")


if __name__ == "__main__":
    # 示例：加载数据集并并行爬取IUPAC名称
    json_file_path = "/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation.json"  # 替换为你的JSON文件路径
    train_data, test_data = load_custom_dataset(json_file_path)
    start_index = 0  # 起始索引
    length = 1000  # 批量处理的大小
    max_len = len(train_data)  # 数据集的最大长度
    print(f"数据集的最大长度：{max_len}")
    for i in range(start_index, max_len, length):
        output_file = f'/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation/test_m_d_g_{i}_{i+length}.json'
        failed_indexes_file = f'/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation/test_failed_indexes_{i}_{i+length}.txt'
        get_iupac_index_range(i, length, train_data, max_len, output_file,failed_indexes_file)
        time.sleep(120)  # 每批次之间暂停2分钟，避免请求过于频繁
        
