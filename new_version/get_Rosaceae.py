
# coding: utf-8

# In[1]:

import lxml.html
import requests
import os
family = "Rosaceae"
if not os.path.exists(family):
    os.mkdir(family)


# In[3]:

html = requests.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=" + family + "&lvl=5")


# In[4]:

print(html)
dom = lxml.html.fromstring(html.text)
print(dom.xpath('//*[@title="genus"]/strong')[0].text)


# In[5]:

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


# In[6]:

print(len(ci))


# In[7]:

di = dom.xpath('//*[@type="disc"]')
for i in di:
    for k in list(i):
        if k.tag == "ul":
            break
    else:
        temp = i[0]
        while(temp.getparent() is not None):
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

print(len(di))


# In[9]:

print(di[0].text_content())


# In[10]:

genuses = dom.xpath('//*[@title="genus"]/strong')
genlist = []
for genus in genuses:
    genlist.append(genus.text)
print(len(genlist))


# In[11]:

import pickle
with open(family + "/genuses.pickle", "wb")as fi:
    pickle.dump(genlist, fi)


# In[12]:

with open(family + "/genuses.pickle", "rb")as fi:
    genlist2 = pickle.load(fi)
print(genlist == genlist2)


# In[23]:

from classes2 import MCS_Finder
import os
import time
import pickle
import datetime
start = time.time()
with open(family + "/genuses.pickle", "rb")as fi:
    genlist = pickle.load(fi)
try:
    for genus in genlist:
        if not os.path.exists(family):
            os.mkdir(family)
        if os.path.exists(family + "/" + genus):
            continue
        f = MCS_Finder(genus, family)
        f.make_kcfs(limit=10000)
        print(datetime.datetime.now())
        print(len(os.listdir(family)))
        time.sleep(15)
except:
    os.rmdir(family + "/" + genus)
    print(time.time() - start)
    print(datetime.datetime.now())
    raise
print(time.time() - start)
print(datetime.datetime.now())


# In[22]:

print(genlist[11])


# In[ ]:




# In[1]:

from classes2 import control_all_genus


# In[2]:

cag = control_all_genus("Rosaceae")


# In[4]:

cag.ari


# In[5]:

print(len(cag.ari))


# In[6]:

glen = []
for genus in cag.ari:
    with open("Rosaceae/" + genus + "/kcfs.kcfs")as f:
        Cnlist = []
        molecule = f.read().split("///\n")
        for mol in molecule[:-1]:
            Cn = mol.split("\n")[0].split()[1]
            Cnlist.append(Cn)
        glen.append((genus, len(Cnlist)))


# In[7]:

sorted(glen, reverse=True, key=lambda x: x[1])


# In[8]:

sorted(cag.get_number_of_Cnumber().items(), reverse = True, key =lambda x: x[1]) 


# In[9]:

specific = cag.get_specifics()
s = sorted(specific.items(), reverse=True, key=lambda x: x[1])
s


# In[10]:

spedict = cag.get_Cnumber_from_label(s[0][0][1])
print(spedict)


# In[11]:

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
for z, i in enumerate(sorted(list(spedict.items())[0][1])):
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


# In[12]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(spedict.items())[0][1]), subImgSize=(400, 400))
img.save("Rosa_test.png")


# さすがにbondで抜き出すとめちゃくちゃ

# In[12]:

for i, k in enumerate(s):
    if k[0][0] == "SKELETON":
        print(k)
        speske = k
        break


# bondと混ざるのでダメ

# In[15]:

for i, k in enumerate(s):
    if k[0][0] == "SKELETON":
        if len(k[0][1].split("-")) < 3:
            continue
        print(k)
        speske = k
        break


# In[14]:

spedict2 = cag.get_Cnumber_from_label(k[0][1])
print(spedict2)


# In[16]:

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
for z, i in enumerate(sorted(list(spedict2.items())[0][1])):
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


# In[17]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(spedict2.items())[0][1]), subImgSize=(400, 400))
img.save("dotpng/Rosa_test2-2.png")


# In[18]:

from nxrd.Compound import Compound


# In[19]:

comp = []
for i in mol_list:
    temp = Compound()
    temp.input_rdkmol(i)
    comp.append(temp)


# In[20]:

print(comp)


# In[21]:

vec = []
for i in comp:
    vec.append(kcfco.kcf_vec(i))


# In[22]:

print(vec)


# In[23]:

vec[0].pandas()


# In[24]:

pan = vec[0].pandas()


# In[25]:

pan.iloc[:, 0]


# In[26]:

veclist = list(pan.iloc[:, 0])


# In[27]:

print(veclist)


# In[28]:

sort = sorted(veclist, reverse=True, key=lambda x: len(x.split("-")))


# In[29]:

print(sort[0])


# 理想的には全部繋がってるやつが欲しいはず。

# In[30]:

print(sort[3])


# In[ ]:




# In[31]:

from tools import make_kcfs


# In[13]:

path = "Rosaceae/" + list(spedict2.items())[0][0] + "/co"


# In[33]:

make_kcfs(list(spedict2.items())[0][1], path)


# In[14]:

kosuu = dict()
with open(path + "splitedcount.txt")as f:
    units = f.read().split("\n")
    for unit in units[:-1]:
        temp = unit.split()
        kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])
sorted(kosuu.items(), reverse=True, key=lambda x: x[1])


# In[15]:

print(len(list(spedict2.items())[0][1]))


# In[17]:

import tools


# In[21]:

all1 = tools.search_all_Cnumber_from_label("C1x-C1x-C1x-C1z-C1y-C1z")
print(all1)


# 結構複雑な構造なのにこんなにあるのは予想外  
# ringのみを抜き出すように変更したい。

# In[60]:

all2 = tools.search_all_Cnumber_from_label('C1(C1)-C1-C1-C1-C1(C1)(C1)-C1-C1-C1-C1-C1-C2-C2')
print(all2)
print(len(all2))


# In[61]:

all3 = tools.search_all_Cnumber_from_label('C1-C1-C1-C1-C1-N1-C1-C1')
print(all3)
print(len(all3))


# In[ ]:

for i in kosuu.items():
    if i[1] >= 10:
        print(i)
        print(len(tools.search_all_Cnumber_from_label(i[0][1])))


# In[1]:

import tools


# In[3]:

len(tools.search_all_Cnumber_from_label('C-C-C-C-C-N', ring=True))


# ringオプションを追加した  
# これで回転も考慮できる。

# In[28]:

import time
s = time.time()
print(len(list(kosuu.items())))
for i in kosuu.items():
    if i[1] >= 10:
        if i[0][0] == "RING":
            temp1, temp2 = tools.search_all_Cnumber_from_label(i[0][1], ring=True)
        else:
            temp1, temp2 = tools.search_all_Cnumber_from_label(i[0][1])
        if i[1] >= temp2/2:  
            print(i)
            print(temp2)
        print(time.time() - s)
print("finish")
print(time.time() - s)


# In[31]:

q = ('RING', 'C1-C1-C1-C1-C1-C1-C1-O2-C1-N1-C1-C1')
if q[0] == "RING":
    temp = tools.search_all_Cnumber_from_label(q[1], ring=True)
else:
    temp = tools.search_all_Cnumber_from_label(q[1])
print(temp)


# In[32]:

print(kosuu[q])


# In[29]:

q = ('RING', 'C1-C1-C1-C1-O2-C1-C1-C1-C2-C1')
if q[0] == "RING":
    temp2 = tools.search_all_Cnumber_from_label(q[1], ring=True)
else:
    temp2 = tools.search_all_Cnumber_from_label(q[1])
print(temp2)


# In[34]:

print(len(temp[0]))
print(len(temp2[0]))


# 時間はかなりかかるようになったが、回転に対応した。  
# 回転する必要のないものを弾く方法も考えておく。

# In[41]:

Cnlist = list(spedict2.items())[0][1]


# In[42]:

for i in temp:
    if i in Cnlist:
        print(i)


# In[43]:

print(path)


# In[19]:

import importlib


# In[26]:

importlib.reload(tools)


# In[ ]:



