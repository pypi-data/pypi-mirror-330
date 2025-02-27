from craft_mol.batch_feature import BatchFeature
import os

model_path = './craft_mol/1m_checkpoint_09.pth'
data_path = '/home/hukun/code/Tmm-llama/data/ChEBI-20-MM/test.csv'
output_dir = '/home/hukun/code/Tmm-llama/data/ChEBI-20-MM/test_mol_features'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
batch_size = 32
config_path = './craft_mol/inference.yaml'
batch_feature = BatchFeature(model_path=model_path, config_path=config_path)
# smiles = "C[C@@H1]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#C[C@H1](C)O)O[C@H1]1CN(C)C(=O)NC(C)C)[C@@H1](C)CO"
# iupac_name = "1-[[(4R,5R)-8-[(3S)-3-hydroxybut-1-ynyl]-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1lambda6,2-benzoxathiazocin-5-yl]methyl]-1-methyl-3-propan-2-ylurea"
# mol_feature = batch_feature.get_feature_single(smiles=smiles, iupac_name=iupac_name)
# print(mol_feature.shape)
batch_feature.get_feature(data_path, 
                          batch_size, 
                          output_dir,
                          CID_name='CID',
                          smiles_name='SMILES',
                          iupac_name='iupacname',
                          selfies_name='SELFIES')
