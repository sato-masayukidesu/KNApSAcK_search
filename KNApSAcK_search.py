
# coding: utf-8

# In[4]:

import urllib.request


# In[19]:

x = input()
url = "http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=%s" % (x)


# In[3]:

print(url)


# In[4]:

urllib.request.urlretrieve(url, '%s.txt' % (x))


# In[20]:

ld = open("%s.txt" % (x))
lines = ld.readlines()
ld.close()

C_number = []

for line in lines:
    if line.find("word=C") >= 0:
        print(line[49:-34])
        C_number.append(line[49:-34])
        urllib.request.urlretrieve("http://knapsack3d.sakura.ne.jp/mol3d/%s.3d.mol" % (line[49:-34]), '%s.mol' % (line[49:-34]))


# In[6]:

print(C_number)


# In[23]:

from rdkit import Chem
for i in C_number:
    mol_data = open('%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    print(Chem.MolToSmiles(mol))


# In[22]:

from rdkit.Chem import Draw
from rdkit.Chem import rdDepictor
for i in C_number:
    mol_data = open('%s.mol' % (i),'r').read()
    mol = Chem.MolFromMolBlock(mol_data)
    rdDepictor.Compute2DCoords(mol)
    Draw.MolToFile(mol, '%s.png' % (i))


# In[ ]:

k = open(copy1.mol, "r").read()
mol = Chem.MolFromMolBlock(k)
rdDepictor.Compute2DCoords(mol)
Draw.MolToFile(mol, '.png' % (i))


# In[ ]:



