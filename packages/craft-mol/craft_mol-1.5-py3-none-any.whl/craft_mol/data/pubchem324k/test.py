import torch
from torch_geometric.data import InMemoryDataset


class PubChemDataset(InMemoryDataset):
    def __init__(self, path):
        super(PubChemDataset, self).__init__()
        self.data, self.slices = torch.load(path)
    
    def __getitem__(self, idx):
        return self.get(idx)


data = PubChemDataset('/home/hukun/code/Tmm-llama/data/PubChem324kV2/PubChem324kV2/pretrain.pt')
print(data[0])


import pubchempy
smi = data[0]["smiles"]
compounds = pubchempy.get_compounds(smi, namespace='smiles')
match = compounds[0]
iupac_name = match.iupac_name
print(iupac_name)

