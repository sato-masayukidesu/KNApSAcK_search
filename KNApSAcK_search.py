
# coding: utf-8

# In[1]:

import urllib.request


# In[2]:

x = input()
url = "http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=%s" % (x)


# In[3]:

print(url)


# In[4]:

urllib.request.urlretrieve(url, '%s.txt' % (x))


# In[7]:

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

print(C_number)


# In[12]:

from rdkit import Chem
mol_data = open('C00000730.mol','r').read()
mol = Chem.MolFromMolBlock(mol_data)
print(Chem.MolToSmiles(mol))


# In[ ]:

C=C(OC1C=C(C(=O)O)C=CC1N)C(=O)O

