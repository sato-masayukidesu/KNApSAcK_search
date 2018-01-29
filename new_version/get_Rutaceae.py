
# coding: utf-8

# In[ ]:

import lxml.html
import requests
import os
family = "Rutaceae"
if not os.path.exists(family):
    os.mkdir(family)


# In[2]:

html = requests.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=" + family + "&lvl=5")


# In[8]:

print(html)


# In[9]:

dom = lxml.html.fromstring(html.text)
print(dom.xpath('//*[@title="genus"]/strong')[0].text)


# In[10]:

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

print(ci)


# In[11]:

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


# In[12]:

print(di)


# In[13]:

di[0].attrib["title"]


# In[14]:

genuses = dom.xpath('//*[@title="genus"]/strong')


# In[15]:

genlist = []
for genus in genuses:
    genlist.append(genus.text)
print(len(genlist))


# In[16]:

import pickle
with open(family + "/genuses.pickle", "wb")as fi:
    pickle.dump(genlist, fi)


# In[3]:

with open(family + "/genuses.pickle", "rb")as fi:
    genlist2 = pickle.load(fi)
print(genlist == genlist2)


# In[19]:

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
        f.make_kcfs()
        print(datetime.datetime.now())
        print(len(os.listdir(family)))
        time.sleep(15)
except:
    print(time.time() - start)
    print(datetime.datetime.now())
    raise
print(time.time() - start)
print(datetime.datetime.now())


# ミカン科抜き終わり。

# In[20]:

from classes2 import control_all_genus


# In[21]:

cag = control_all_genus("Rutaceae")


# In[22]:

cag.ari


# 明らかにおかしいので修正する

# In[6]:

import requests
import lxml.html


# In[7]:

html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word=acronychia")


# In[8]:

print(html)


# In[9]:

dom = lxml.html.fromstring(html.text)


# In[10]:

dom.xpath('//*[@id="my_contents"]/font[2]')[0].text


# In[13]:

dom.xpath('//*[@class="sortable d1"]/tr[2]/td[1]/a')[0].text


# In[17]:

str(dom.xpath('//*[@class="sortable d1"]/tr[2]/td[6]/font')[0].text_content())


# In[18]:

html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word=sus")


# In[19]:

dom = lxml.html.fromstring(html.text)


# In[20]:

dom.xpath('//*[@id="my_contents"]/font[2]')[0].text


# In[24]:

str(dom.xpath('//*[@class="sortable d1"]/tr[1]/td[6]')[0].text_content()).split()[0]


# 修正完了

# In[ ]:




# In[2]:

from classes2 import control_all_genus


# In[3]:

cag = control_all_genus("Rutaceae")


# In[4]:

cag.ari


# In[5]:

print(len(cag.ari))


# In[6]:

sorted(cag.get_number_of_Cnumber().items(), reverse = True, key =lambda x: x[1]) 


# In[7]:

import tools


# In[8]:

ge = tools.get_genuses("C00002198")


# In[9]:

print(ge)


# In[10]:

ge2 = set()
for i in ge[2:]:
    ge2.add(i.split()[0])
print(len(ge2))


# In[11]:

print(ge2)


# In[12]:

for i in ge2:
    if i in cag.ari:
        continue
    print(i)


# In[13]:

for i in ge:
    if i.split()[0] == "Fagara":
        print(i)


# ncbiには載っていない属もあった。  
# とりあえず放置

# In[14]:

sorted(cag.get_split_kcfs().items(), reverse=True, key=lambda x: x[1])


# In[15]:

specific = cag.get_specifics()
s = sorted(specific.items(), reverse=True, key=lambda x: x[1])
s


# In[16]:

spedict = cag.get_Cnumber_from_label(s[0][0][1])
print(spedict)


# In[17]:

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


# In[46]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(spedict.items())[0][1]), subImgSize=(400, 400))
img.save("Ruta_test.png")


# In[18]:

for i, k in enumerate(s):
    if k[0][0] == "SKELETON":
        print(k)
        speske = k
        break


# In[19]:

spedict2 = cag.get_Cnumber_from_label(k[0][1])
print(spedict2)


# In[20]:

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


# In[23]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(spedict2.items())[0][1]), subImgSize=(400, 400))
img.save("Ruta_test2.png")


# In[21]:

from tools import make_kcfs


# In[22]:

path = "Rutaceae/" + list(spedict2.items())[0][0] + "/" + list(spedict2.items())[0][0]
print(path)


# In[26]:

make_kcfs(list(spedict2.items())[0][1], path)


# In[23]:

print(len(list(spedict2.items())[0][1]))


# In[27]:

kosuu = dict()
with open(path + "splitedcount.txt")as f:
    units = f.read().split("\n")
    for unit in units[:-1]:
        temp = unit.split()
        kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])
sorted(kosuu.items(), reverse=True, key=lambda x: x[1])


# In[28]:

print(len(list(spedict2.items())[0][1]))


# 共発現しているのは14って書いてあるところ周辺

# In[29]:

all1 = tools.search_all_Cnumber_from_label('C8x-C8x-C8x-C8x-C8y-C8y-C8y-N4x-C8y')
print(len(all1))


# In[30]:

all2 = tools.search_all_Cnumber_from_label('C8x-C8y-C8y-C8y-C8y-C8y-N4x-C8y-C8y')
print(len(all2))


# In[31]:

print(all2)


# In[32]:

for i in all2:
    if i in list(spedict2.items())[0][1]:
        continue
    print(i)


# In[33]:

print("Murraya" in cag.ari)


# In[34]:

tools.make_kcfs2(list(spedict2.items())[0][1], path)


# In[36]:

import importlib
importlib.reload(tools)


# In[37]:

kosuu = dict()
with open(path + "splitedcount.txt")as f:
    units = f.read().split("\n")
    for unit in units[:-1]:
        temp = unit.split()
        kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])
sorted(kosuu.items(), reverse=True, key=lambda x: x[1])


# In[ ]:




# 気になったのでO-P-Oもやる。

# In[38]:

s2 = s[1]
print(s2)


# In[40]:

spedict3 = cag.get_Cnumber_from_label(s2[0][1])
print(spedict3)


# In[41]:

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
for z, i in enumerate(sorted(list(spedict3.items())[0][1])):
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


# In[42]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(spedict3.items())[0][1]), subImgSize=(400, 400))
img.save("Ruta_test3.png")


# In[ ]:



