
# coding: utf-8

# In[1]:

import lxml.html
import requests
import os
if not os.path.exists("Fabaceae"):
    os.mkdir("Fabaceae")


# In[2]:

html = requests.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=Fabaceae&lvl=5")


# In[3]:

print(html)


# In[4]:

dom = lxml.html.fromstring(html.text)


# In[5]:

print(dom.xpath('//*[@title="genus"]/strong')[0].text)


# In[6]:

ci = dom.xpath('//*[@type="circle"]')
for i in ci:
    for k in list(i):
        if k.tag == "ul":
            break
    else:
        temp = i
        flag = True
        while(temp.getparent() is not None):
            try:
                if temp.tag == "li":
                    if temp.xpath("a")[0].attrib["title"] == "genus":
                        flag = False
                        break
                    else:
                        temp = temp.getparent()
                else:
                    temp = temp.getparent()
                    # print("genus")
            except (KeyError, IndexError):
                temp = temp.getparent()
        else:
            print(i.text_content())


# In[7]:

di = dom.xpath('//*[@type="disc"]')
for i in di:
    for k in list(i):
        if k.tag == "ul":
            break
    else:
        temp = i[0]
        while(temp.getparent()):
            try:
                if temp.attrib["title"] == "genus":
                    break
                else:
                    temp = temp.getparent()
                    print("genus")
            except:
                temp = temp.getparent()
        else:
            print(i.text_content())


# In[8]:

print(di)


# In[9]:

genuses = dom.xpath('//*[@title="genus"]/strong')


# In[10]:

genlist = []
for genus in genuses:
    genlist.append(genus.text)


# In[11]:

print(len(genlist))


# In[12]:

print(genlist)


# In[17]:

import pickle
with open("Fabaceae/genuses.pickle", "wb")as fi:
    pickle.dump(genlist, fi)


# In[13]:

from classes2 import MCS_Finder
import os
import time
import pickle
import datetime
start = time.time()
with open("Fabaceae/genuses.pickle", "rb")as fi:
    genlist = pickle.load(fi)
try:
    for genus in genlist:
        if not os.path.exists("Fabaceae"):
            os.mkdir("Fabaceae")
        if os.path.exists("Fabaceae/" + genus):
            continue
        f = MCS_Finder(genus, "Fabaceae")
        f.make_kcfs()
        print(datetime.datetime.now())
        print(len(os.listdir("Fabaceae")))
        time.sleep(15)
except:
    print(time.time() - start)
    print(datetime.datetime.now())
    raise
print(time.time() - start)
print(datetime.datetime.now())


# 抜き終わり

# In[ ]:




# In[14]:

import os
print(len(os.listdir("Fabaceae")))


# In[15]:

import pickle
with open("Fabaceae/genuses.pickle", "rb")as fi:
    genlist = pickle.load(fi)
print(len(genlist))


# In[1]:

from classes2 import control_all_genus


# In[2]:

cag = control_all_genus("Fabaceae")


# In[3]:

cag.ari


# In[4]:

print(len(cag.ari))


# In[5]:

glen = []
for genus in cag.ari:
    with open(cag.path + "/" + genus + "/kcfs.kcfs")as f:
        Cnlist = []
        molecule = f.read().split("///\n")
        for mol in molecule[:-1]:
            Cn = mol.split("\n")[0].split()[1]
            Cnlist.append(Cn)
        glen.append((genus, len(Cnlist)))
sorted(glen, reverse=True, key=lambda x: x[1])


# In[6]:

sorted(cag.get_number_of_Cnumber().items(), reverse = True, key =lambda x: x[1]) 


# In[7]:

sorted(cag.get_split_kcfs().items(), reverse=True, key=lambda x: x[1])


# In[8]:

specific = cag.get_specifics()
s = sorted(specific.items(), reverse=True, key=lambda x: x[1])
s


# In[9]:

print(cag.get_Cnumber_from_label('C1x-N1y-C1z'))


# In[10]:

Ery = cag.get_Cnumber_from_label('C1x-N1y-C1z')


# In[28]:

hanni = []
for i in range(1, 52):
    page = str(i)
    with open("../../../database/knapsack-kcf/KNApSAck" + page + ".kcf")as f1:
        clist = f1.read().split()
        hanni.append(clist[1])

import sys
sys.path.append("../../module")
from rdkit.Chem import rdDepictor
import kcf.converter as kcfco
from rdkit import Chem
mol_list = []
counter = 0
nCnumber = []
for z, i in enumerate(sorted(list(Ery.items())[0][1])):
    num = int(i[1:])
    for p, k in enumerate(hanni[1:]):
        k2 = int(k[1:])
        if k2 > num:
            k3 = str(p+1)
            with open("../../../database/knapsack-kcf/KNApSAck" + k3 + ".kcf")as f2:
                Clist = f2.read().split("///\n")
                try:
                    for C in Clist:
                        if i == C.split()[1]:
                            molblock = kcfco.kcf_to_molblock(C)
                            # print("OK", i)
                            # print(molblock[1])
                            mol = Chem.MolFromMolBlock(molblock[1])
                            if mol is None:
                                print("None", i, z, k3)
                                if "#+" in C or "#-" in C:
                                    print("Charge in\n")
                                counter += 1
                                break
                            rdDepictor.Compute2DCoords(mol)
                            mol_list.append(mol)
                            nCnumber.append(i)
                            if "#+" in C or "#-" in C:
                                print(i, z, k3, "Charge in\n")
                            break
                except IndexError:
                    counter += 1
                    print("DAME", i, z)
            break
print(counter)


# In[29]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(Ery.items())[0][1]), subImgSize=(400, 400))
img.save("Faba_test-2.png")


# In[11]:

from tools import search_all_Cnumber_from_label


# In[12]:

ac = search_all_Cnumber_from_label('C1x-N1y-C1z')


# In[15]:

print(len(ac[0]))


# In[16]:

from tools import make_kcfs


# In[17]:

print(Ery)


# In[27]:

print(len(list(Ery.items())[0][1]))


# In[18]:

path = "Fabaceae/" + list(Ery.items())[0][0] + "/" + list(Ery.items())[0][0]
print(path)


# In[19]:

make_kcfs(list(Ery.items())[0][1], path)


# In[29]:

kosuu = dict()
with open(path + "splitedcount.txt")as f:
    units = f.read().split("\n")
    for unit in units[:-1]:
        temp = unit.split()
        if temp[1] == "ATOM" or temp[1] == "BOND":
            continue
        kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])
sorted(kosuu.items(), reverse=True, key=lambda x: x[1])


# In[33]:

test = list(Ery.items())[0][1]


# In[34]:

test2 = cag.gCfl(list(Ery.items())[0][0], 'C-C-C-C-C(C-C)-C-C-C(C-C)-C-C-C-C')


# In[38]:

test3 = []
for i in test:
    if i in test2:
        test3.append(i)
    else:
        print(i)


# In[36]:

print(test3)


# In[37]:

print(len(test), len(test2), len(test3))


# In[ ]:



