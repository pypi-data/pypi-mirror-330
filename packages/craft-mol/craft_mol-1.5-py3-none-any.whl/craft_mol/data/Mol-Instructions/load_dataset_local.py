import json
import os

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


json_file_path = "/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/data/Molecule-oriented_Instructions/molecular_description_generation.json"
train_data, test_data = load_custom_dataset(json_file_path)

# 打印加载的 train 和 test 数据的前 2 条样本
print("Train Data (First 2 samples):")
print(train_data[:2])

print("\nTest Data (First 2 samples):")
print(test_data[:2])
