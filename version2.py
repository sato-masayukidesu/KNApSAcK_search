
# coding: utf-8

# In[9]:

import urllib.request
import os
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from rdkit.Chem import BRICS
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import rdFMCS


# In[2]:

x = input()
url = "http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=%s" % (x)


# In[3]:

try:
    os.mkdir(x)
except FileExistsError:
    pass


# In[4]:

os.chdir(x)


# In[5]:

urllib.request.urlretrieve(url, '%s.txt' % (x))


# In[6]:

ld = open("%s.txt" % (x))
lines = ld.readlines()
ld.close()

C_number = []

for line in lines:
    if line.find("word=C") >= 0:
        print(line[49:-34])
        C_number.append(line[49:-34])
        urllib.request.urlretrieve("http://knapsack3d.sakura.ne.jp/mol3d/%s.3d.mol" % (line[49:-34]), '%s.mol' % (line[49:-34]))


# In[8]:

mols = []
for i in C_number:
    mol_data = open('%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    mols.append(mol)
outf = Chem.SDWriter("output.sdf")
for mol in mols:
    AllChem.Compute2DCoords(mol)
    outf.write(mol)


# In[10]:

ms = [m for m in Chem.SDMolSupplier('output.sdf') if m is not None]
mcs = rdFMCS.FindMCS(ms)
mcs_smarts = mcs.smartsString
mcs_mol = Chem.MolFromSmarts(mcs_smarts)
for i,m in enumerate(ms):
    match_atoms = m.GetSubstructMatch(mcs_mol)
    print (match_atoms)
    Draw.MolToFile(m,'comp_%d.png' % i,highlightAtoms=match_atoms)


# In[ ]:



