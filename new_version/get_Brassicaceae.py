
# coding: utf-8

# In[1]:

import lxml.html
import requests


# In[2]:

html = requests.get("https://ja.wikipedia.org/wiki/アブラナ科")


# In[3]:

print(html)


# In[4]:

dom = lxml.html.fromstring(html.text)


# In[5]:

print(dom.xpath('//*[@id="mw-content-text"]/div/ul[1]/li[1]/ul/li/i/span/a')[0].text)


# In[6]:

genus = dom.xpath('//*[@id="mw-content-text"]/div/ul[1]/li/ul/li/i/span/a')


# In[7]:

len(genus)


# In[8]:

for i in genus:
    print(i.text)


# In[9]:

gtxt = []
for i in genus:
    gtxt.append(i.text)


# In[10]:

print(sorted(gtxt))


# In[11]:

html = requests.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=Brassicaceae")


# In[12]:

print(html)


# In[13]:

dom = lxml.html.fromstring(html.text)


# In[8]:

print(list(dom.xpath('/html/body/form')[0]))


# In[10]:

print(html.text)


# In[14]:

print(dom.xpath('//*[@title="genus"]/strong')[0].text)


# In[15]:

genuses = dom.xpath('//*[@title="genus"]/strong')


# In[16]:

genlist = []
for genus in genuses:
    genlist.append(genus.text)


# In[17]:

print(len(genlist))


# In[18]:

import pickle
with open("Brassicaceae/genuses.pickle", "wb")as fi:
    pickle.dump(genlist, fi)


# In[19]:

with open("Brassicaceae/genuses.pickle", "rb")as fi:
    genlist2 = pickle.load(fi)
print(genlist == genlist2)


# In[20]:

di = dom.xpath('//*[@type="disk"]')
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


# In[21]:

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


# In[23]:

from classes2 import MCS_Finder
import os
import time
import pickle
import datetime
start = time.time()
with open("Brassicaceae/genuses.pickle", "rb")as fi:
    genlist = pickle.load(fi)
try:
    with open("Brassicaceae/genuses.pickle", "rb")as fi:
        genlist2 = pickle.load(fi)
    for genus in genlist:
        if not os.path.exists("Brassicaceae"):
            os.mkdir("Brassicaceae")
        if os.path.exists("Brassicaceae/" + genus):
            continue
        f = MCS_Finder(genus, "Brassicaceae")
        f.make_kcfs()
        time.sleep(15)
except:
    print(time.time() - start)
    print(datetime.datetime.now())
    raise
print(time.time() - start)
print(datetime.datetime.now())


# In[24]:

print(genlist[-21])


# In[ ]:




# 抜き終わった

# In[25]:

import os
print(len(os.listdir("Brassicaceae")))


# In[26]:

import pickle
with open("Brassicaceae/genuses.pickle", "rb")as fi:
    genlist = pickle.load(fi)
print(len(genlist))


# In[27]:

ari = []
for genus in os.listdir("Brassicaceae"):
    if genus == ".DS_Store" or genus == "others" or genus == "genuses.pickle":
        continue
    elif os.listdir("Brassicaceae/" + genus) == []:
        continue
    else:
        ari.append(genus)


# In[28]:

print(len(ari)) 


# In[113]:

di = dom.xpath('//*[@type="circle"]')


# In[114]:

for i in di:
    for k in list(i):
        if k.tag == "ul":
            break
    else:
        if i[0].attrib["title"] != "species":
            print(i.text_content())


# In[29]:

print(ari)


# In[31]:

def get_all_cnumber_from_kcfs(genus):
    with open("Brassicaceae/" + genus + "/kcfs.kcfs")as f:
        Cnlist = []
        molecule = f.read().split("///\n")
        for mol in molecule[:-1]:
            Cn = mol.split("\n")[0].split()[1]
            Cnlist.append(Cn)
    return Cnlist


# In[32]:

arilist = []
for genus in ari:
    arilist.append(get_all_cnumber_from_kcfs(genus))


# In[33]:

kosuu = dict()
for Cnlist in arilist:
    for Cn in Cnlist:
        kosuu[Cn] = kosuu.get(Cn, 0) + 1


# In[34]:

counter = 0
for i in kosuu.items():
    if i[1] > 1:
        print(i)
        counter += i[1] -1
print(len(kosuu)-counter)


# In[35]:

sorted(kosuu.items(), reverse=True, key=lambda x: x[1])


# In[36]:

total = 0
for i in kosuu.items():
    total += i[1]
print(total)


# In[37]:

kosuu2 = dict()
for genus in ari:
    with open("Brassicaceae/" + genus + "/splitedcount.txt")as f:
        units = f.read().split("\n")
        for unit in units[:-1]:
            temp = unit.split()
            kosuu2[(temp[1], temp[2])] = kosuu2.get((temp[1], temp[2]), 0) + int(temp[3])


# In[38]:

sorted(kosuu2.items(), reverse=True, key=lambda x: x[1])


# In[1]:

from classes2 import control_all_genus


# In[2]:

cag = control_all_genus("Brassicaceae")


# In[3]:

cag.ari


# In[4]:

cag.get_number_of_Cnumber()


# In[5]:

sorted(cag.get_number_of_Cnumber().items(), reverse = True, key =lambda x: x[1]) 


# In[6]:

kosuu12 = cag.get_number_of_Cnumber()
for x in kosuu:
    if kosuu[x] != kosuu12[x]:
        print(x)
        break
else:
    print("OK")


# In[7]:

cag.get_all_kcfs()


# In[8]:

sorted(cag.get_split_kcfs().items(), reverse=True, key=lambda x: x[1])


# In[9]:

specific = cag.get_specifics()


# In[10]:

s = sorted(specific.items(), reverse=True, key=lambda x: x[1])


# In[11]:

s


# In[12]:

Cngenus = dict()
for genus in cag.ari:
    with open("Brassicaceae/" + genus + "/kcfs.kcfs")as fi:
        molecule = fi.read().split("///\n")
        Cngenus[genus] = len(molecule)


# In[13]:

sorted(Cngenus.items(), reverse=True, key=lambda x: x[1])


# In[14]:

print(cag.get_Cnumber_from_label("C-C-C-C-C-N-Z-N-C"))


# In[15]:

print(cag.get_Cnumber_from_label("C1y-C1b-O2b"))


# In[16]:

print(cag.get_Cnumber_from_label("N4x-C8y-O5x"))


# In[17]:

for S in s:
    if S[1][1] != "Arabidopsis":
        print(S)


# In[18]:

print(cag.get_Cnumber_from_label("C8y(C1b+N4x+N5x)"))


# In[19]:

print(cag.get_Cnumber_from_label("C8-C8-C8-C8-C8-C8-C1-C8"))


# In[20]:

print(cag.get_Cnumber_from_label("C8-C1-C8-C8-C8-C8-C8-C8"))


# In[21]:

print(cag.get_Cnumber_from_label("O1c-P1b(O2b)(O1c)-O2c-P1b(O2b)(O1c)-O1c"))


# In[22]:

print(len(cag.ari))


# In[23]:

test = cag.get_Cnumber_from_label("C8-C8-C8-C8-C8-C8-C1-C8")


# In[26]:

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
for z, i in enumerate(sorted(list(test.items())[0][1])):
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
                            # rdDepictor.Compute2DCoords(mol)
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


# In[27]:

list(test.items())[0][1]


# In[28]:

print(mol_list)


# In[29]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(test.items())[0][1]), subImgSize=(400, 400))
img.save("Brassi_test.png")


# 属中の種の数とか知りたい  
# classes.toolsを作りたい。

# In[30]:

print(cag.get_Cnumber_from_label("C1a-C1z-C5x"))


# In[31]:

from tools import search_all_Cnumber_from_label
from tools import get_genuses
from tools import get_name


# In[32]:

ac = search_all_Cnumber_from_label("C1a-C1z-C5x")


# In[35]:

print(len(ac[0]))


# In[36]:

ac2 = search_all_Cnumber_from_label("C8-C8-C8-C8-C8-C8-C1-C8")


# In[75]:

print(len(ac2))


# In[37]:

print(len(ac2[0]))


# In[38]:

print(ac2)


# 7/12がLepidiumに入っていた。

# In[41]:

import time
name = []
for Cn in ac2[0]:
    time.sleep(5)
    name.append(get_genuses(Cn))
    print(Cn)
print(name)


# In[43]:

ac2name = dict()
for x, y in zip(ac2[0], name):
    ac2name[x] = y
print(ac2name)


# In[46]:

sorted(list(ac2name.items()))


# 前の5つがlepidiumの持ってないやつ。  
# さらに5つめは存在しなかった。  
# しかもおそらく入力ミスでsatisvumは存在しない。

# In[79]:

from tools import make_kcfs


# In[80]:

print(test)


# In[81]:

test2 = list(test.values())[0]


# In[82]:

make_kcfs(test2, "Brassicaceae/Lepidium/Lepidium")


# In[83]:

path = "Brassicaceae/Lepidium/Lepidium"
kosuu = dict()
with open(path + "splitedcount.txt")as f:
    units = f.read().split("\n")
    for unit in units[:-1]:
        temp = unit.split()
        kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])
print(kosuu)


# In[84]:

sorted(kosuu.items(), reverse=True, key=lambda x: x[1])


# 共発現していそうなのはC8x-C8x-N4x-C8y-N5xとC8-C8-C8-C8-C8-C8-C1-C8である。

# In[85]:

kyou = search_all_Cnumber_from_label("C8x-C8x-N4x-C8y-N5x")


# In[86]:

for k in kyou:
    if not k in test["Lepidium"]:
        print(k)


# In[87]:

import time
name2 = []
for Cn in ["C00026987", "C00026988"]:
    time.sleep(5)
    name2.append(get_genuses(Cn))
print(name2)


# In[88]:

res = []
label = "C8x-C8x-N4x-C8y-N5x"
for i in label.split("-"):
    res.append(i[:2])
lev2 = "-".join(res)
print(lev2)


# In[89]:

kyou2 = search_all_Cnumber_from_label(lev2)


# In[90]:

print(kyou2)


# In[91]:

for i in test["Lepidium"]:
    if i not in kyou2:
        print(i)


# 何個か見てみたが、五員環のくっついている位置が違った。

# In[92]:

import simnet2


# In[93]:

import importlib
simnet2 = importlib.reload(simnet2)


# In[77]:

Clist = test["Lepidium"]
print(Clist)


# In[95]:

simnet2.get_simcomp(Clist)


# In[78]:

get_ipython().magic('matplotlib inline')
simnet2.make_graph(Clist, mode=0, lim=0.8)


# In[103]:

for i in Clist:
    print("http://rest.genome.jp/simcomp/" + i + "/knapsack/cutoff=0.8")


# In[ ]:




# In[49]:

s


# In[50]:

for S in s:
    if S[1][1] == "Brassica":
        print(S)


# In[53]:

CnB = cag.get_Cnumber_from_label("N1b-C2c-S2a")


# In[54]:

print(CnB)


# In[51]:

ac3 = search_all_Cnumber_from_label("N1b-C2c-S2a")


# In[52]:

print(ac3)


# In[65]:

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
for z, i in enumerate(sorted(list(CnB.items())[0][1])):
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


# In[66]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(CnB.items())[0][1]), subImgSize=(400, 400))
img.save("dotpng/Brassi_test2.png")


# In[67]:

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
for z, i in enumerate(sorted(ac3[0])):
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


# In[68]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(ac3[0]), subImgSize=(400, 400))
img.save("dotpng/Brassi_test3.png")


# In[69]:

import simnet2


# In[74]:

print(list(CnB.items())[0][1])


# In[75]:

simnet2.get_simcomp(list(CnB.items())[0][1], "SIMCOMP2/Brassi_test.txt")


# In[95]:

get_ipython().magic('matplotlib inline')
simnet2.make_graph(sorted(list(CnB.items())[0][1]), mode=1, lim=0.8, filepath="SIMCOMP2/Brassi_test.txt")


# In[81]:

sorted(list(CnB.items())[0][1])


# In[94]:

import importlib
importlib.reload(simnet2)


# In[96]:

import time
name = []
for Cn in sorted(list(CnB.items())[0][1]):
    time.sleep(5)
    name.append(get_genuses(Cn))
    print(Cn)
print(name)


# In[97]:

name


# In[1]:

import tools


# In[2]:

tools.search_all_Cnumber_from_label("N1b-C2c-S2a")


# In[3]:

temp = tools.search_all_Cnumber_from_label("N1b-C2c-S2a")


# In[5]:

import time
k = []
for i in temp[0]:
    k.append(tools.get_genuses(i))
    time.sleep(5)
print(k)


# In[6]:

for i1, i2 in zip(k, temp[0]):
    print(i2)
    print(i1, "\n")


# In[ ]:



