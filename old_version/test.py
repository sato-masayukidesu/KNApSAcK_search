
# coding: utf-8

# In[ ]:

C_number = ["C00000730","C00000733","C00000734"]


# In[ ]:

from rdkit import Chem
for i in C_number:
    mol_data = open('%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    print(Chem.MolToSmiles(mol))


# In[ ]:

from rdkit.Chem import Recap
from rdkit.Chem import Draw
mol_data = open('%s.mol' % (C_number[0]),'r').read()
mol = Chem.MolFromMolBlock(mol_data)
node = Recap.RecapDecompose(mol)
print(node)


# In[ ]:

all_nodes = [node.mol for node in node.GetAllChildren().values()]
img = Draw.MolsToGridImage(all_nodes)
img.save('all_nodes.png')


# In[ ]:

leaves = [leaf.mol for leaf in node.GetLeaves().values()]
img = Draw.MolsToGridImage(leaves)
img.save('leaves.png')


# In[ ]:




# In[ ]:

from rdkit.Chem import AllChem
from rdkit.Chem import BRICS
from rdkit.Chem import rdMolDescriptors


# In[ ]:

smiles = Chem.MolToSmiles(mol)
frag = BRICS.BRICSDecompose(mol)


# In[ ]:

print(len(frag))


# In[ ]:

print(frag)


# In[ ]:

from rdkit.Chem import Draw
from rdkit.Chem import rdDepictor
for i in frag:
    mol = Chem.MolFromSmiles(i)
    rdDepictor.Compute2DCoords(mol)
    Draw.MolToFile(mol, '%s.png' % (i))


# In[ ]:




# In[ ]:

for i in C_number:
    mol_data = open('%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    smiles = Chem.MolToSmiles(mol)
    frag = BRICS.BRICSDecompose(mol)
    print(frag)


# In[ ]:

mols = []
for i in C_number:
    mol_data = open('%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    mols.append(mol)
outf = Chem.SDWriter("output.sdf")
for mol in mols:
    AllChem.Compute2DCoords(mol)
    outf.write(mol)


# In[ ]:

from rdkit.Chem import rdFMCS
ms = [m for m in Chem.SDMolSupplier('output.sdf') if m is not None]
mcs = rdFMCS.FindMCS(ms)
mcs_smarts = mcs.smartsString
mcs_mol = Chem.MolFromSmarts(mcs_smarts)
for i,m in enumerate(ms):
    match_atoms = m.GetSubstructMatch(mcs_mol)
    print (match_atoms)
    Draw.MolToFile(m,'comp_%d.png' % i,highlightAtoms=match_atoms)


# In[ ]:



