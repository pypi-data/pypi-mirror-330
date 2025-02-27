from datasets import load_dataset

# 通过 load_dataset 加载数据集（假设你已经定义好了 MyDataset 类）
dataset = load_dataset("/home/hukun/code/trimodal_code/craft_mol/data/Mol-Instructions/Mol-Instructions.py", name="Molecule-oriented Instructions")

# 选择你需要的分割
split = "molecular_description_generation"
data = dataset[split]

# 查看数据
print(data[:5])

# 访问字段
for example in data:
    print(f"Instruction: {example['instruction']}")
    print(f"Input: {example['input']}")
    print(f"Output: {example['output']}")
    print(f"Metadata: {example['metadata']}")
    print("="*50)