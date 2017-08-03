
# coding: utf-8

# In[2]:

C_number = ["C00000730","C00000733","C00000734"]


# In[3]:

from rdkit import Chem
for i in C_number:
    mol_data = open('Klebsiella/%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    print(Chem.MolToSmiles(mol))


# In[4]:

from rdkit.Chem import Recap
from rdkit.Chem import Draw
mol_data = open('Klebsiella/%s.mol' % (C_number[0]),'r').read()
mol = Chem.MolFromMolBlock(mol_data)
node = Recap.RecapDecompose(mol)
print(node)


# In[6]:

all_nodes = [node.mol for node in node.GetAllChildren().values()]
img = Draw.MolsToGridImage(all_nodes)
img.save('all_nodes.png')


# フラグメント化して全部まとめて表示

# In[7]:

leaves = [leaf.mol for leaf in node.GetLeaves().values()]
img = Draw.MolsToGridImage(leaves)
img.save('leaves.png')


# 葉ノードだけ表示

# In[ ]:




# In[8]:

from rdkit.Chem import AllChem
from rdkit.Chem import BRICS
from rdkit.Chem import rdMolDescriptors


# In[21]:

smiles = Chem.MolToSmiles(mol)
frag = BRICS.BRICSDecompose(mol)
print(smiles)


# In[20]:

print(len(frag))


# In[11]:

print(frag)


# In[12]:

from rdkit.Chem import Draw
from rdkit.Chem import rdDepictor
for i in frag:
    mol = Chem.MolFromSmiles(i)
    rdDepictor.Compute2DCoords(mol)
    Draw.MolToFile(mol, '%s.png' % (i))


# In[ ]:




# In[16]:

for i in C_number:
    mol_data = open('Klebsiella/%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    smiles = Chem.MolToSmiles(mol)
    frag = BRICS.BRICSDecompose(mol)
    print(frag)


# In[17]:

mols = []
for i in C_number:
    mol_data = open('Klebsiella/%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    mols.append(mol)
outf = Chem.SDWriter("output.sdf")
for mol in mols:
    AllChem.Compute2DCoords(mol)
    outf.write(mol)


# In[18]:

from rdkit.Chem import rdFMCS
ms = [m for m in Chem.SDMolSupplier('output.sdf') if m is not None]
mcs = rdFMCS.FindMCS(ms)
mcs_smarts = mcs.smartsString
mcs_mol = Chem.MolFromSmarts(mcs_smarts)
for i,m in enumerate(ms):
    match_atoms = m.GetSubstructMatch(mcs_mol)
    print (match_atoms)
    Draw.MolToFile(m,'comp_%d.png' % i,highlightAtoms=match_atoms)


# In[22]:

print(mcs_smarts)


# In[24]:

mcsMol = Chem.MolFromSmarts(mcs_smarts,mergeHs=True)


# In[25]:

Draw.MolToFile(Chem.Mol(mcsMol.ToBinary()),"mcs.png",kekulize=False)


# In[27]:

match_list = []
for i,m in enumerate(ms):
    match_atoms = m.GetSubstructMatch(mcs_mol)
    print (match_atoms)
    match_list.append(match_atoms)
img = Draw.MolsToGridImage(ms, highlightAtomLists=match_list)
img.save('all_comp.png')


# In[28]:

with open("Streptomyces.kcfs")as f:
    file = f.read()
    molecule = file.split("///\n")
    print(mocule[0])


# In[7]:

from rdkit.Chem import rdDepictor
all_nodes = []
for nod in node.GetAllChildren().values():
    rdDepictor.Compute2DCoords(nod.mol)
    all_nodes.append(nod.mol)
img = Draw.MolsToGridImage(all_nodes)
img.save('all_nodes.png')


# In[9]:

leavs = []
for leaf in node.GetLeaves().values():
    rdDepictor.Compute2DCoords(leaf.mol)
    leavs.append(leaf.mol)
img = Draw.MolsToGridImage(leavs)
img.save('leaves.png')


# In[ ]:



