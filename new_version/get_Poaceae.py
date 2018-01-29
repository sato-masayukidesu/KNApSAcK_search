
# coding: utf-8

# In[1]:

import lxml.html
import requests


# In[2]:

html = requests.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=Poaceae&lvl=8")


# In[3]:

print(html)


# In[4]:

dom = lxml.html.fromstring(html.text)


# In[48]:

print(dom.xpath('//*[@title="genus"]/strong')[1].text)


# In[5]:

genuses = dom.xpath('//*[@title="genus"]/strong')


# In[6]:

genlist = []
for genus in genuses:
    genlist.append(genus.text)


# In[7]:

print(len(genlist))


# In[22]:

print(genlist)


# In[9]:

di = dom.xpath('//*[@type="disk"]')


# In[10]:

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


# In[11]:

ci = dom.xpath('//*[@type="circle"]')


# In[ ]:

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


# In[8]:

import pickle
with open("Poaceae/genuses.pickle", "wb")as fi:
    pickle.dump(genlist, fi)


# In[9]:

with open("Poaceae/genuses.pickle", "rb")as fi:
    genlist2 = pickle.load(fi)
print(genlist == genlist2)


# In[10]:

from classes2 import MCS_Finder
import os
import time
import pickle
import datetime
start = time.time()
with open("Poaceae/genuses.pickel", "rb")as fi:
    genlist = pickle.load(fi)
try:
    with open("Poaceae/genuses.pickel", "rb")as fi:
        genlist2 = pickle.load(fi)
    for genus in genlist:
        if not os.path.exists("Poaceae"):
            os.mkdir("Poaceae")
        if os.path.exists("Poaceae/" + genus):
            continue
        f = MCS_Finder(genus, "Poaceae")
        f.make_kcfs()
        print(datetime.datetime.now())
        time.sleep(15)
except:
    print(time.time() - start)
    print(datetime.datetime.now())
    raise
print(time.time() - start)
print(datetime.datetime.now())


# In[14]:

import os
ari = []
for genus in os.listdir("Poaceae"):
    if genus == ".DS_Store" or genus == "others" or genus == "genuses.pickle":
        continue
    elif os.listdir("Poaceae/" + genus) == []:
        continue
    else:
        ari.append(genus)


# In[15]:

print(len(ari))


# In[58]:

len(os.listdir("Poaceae"))


# In[59]:

print(len(genlist))


# In[60]:

for i in os.listdir("Poaceae"):
    if i not in genlist:
        print(i)


# In[54]:

import shutil


# In[57]:

for i in os.listdir("Poaceae"):
    if i == ".DS_Store" or i == "others" or i == "genuses.pickel":
        continue
    if i not in genlist:
        shutil.rmtree("Poaceae/" + i)
        print(i)


# イネ科抜き終わり

# In[2]:

from classes2 import control_all_genus


# In[3]:

cag = control_all_genus("Poaceae")


# In[4]:

len(cag.ari)


# In[5]:

sorted(cag.get_number_of_Cnumber().items(), reverse = True, key =lambda x: x[1]) 


# In[6]:

sorted(cag.get_split_kcfs().items(), reverse=True, key=lambda x: x[1])


# In[7]:

specific = cag.get_specifics()


# In[8]:

spe = sorted(specific.items(), reverse=True, key=lambda x: x[1])


# In[9]:

spe


# In[10]:

Cngenus = dict()
for genus in cag.ari:
    with open("Poaceae/" + genus + "/kcfs.kcfs")as fi:
        molecule = fi.read().split("///\n")
        Cngenus[genus] = len(molecule)
sorted(Cngenus.items(), reverse=True, key=lambda x: x[1])


# In[11]:

print(cag.get_Cnumber_from_label(spe[0][0][1]))


# In[12]:

test = cag.get_Cnumber_from_label(spe[0][0][1])


# In[13]:

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


# In[16]:

from rdkit.Chem import Draw
img = Draw.MolsToGridImage(mol_list, legends=sorted(list(test.items())[0][1]), subImgSize=(400, 400))
img.save("dotpng/Poa_test-2.png")


# In[30]:

from tools import search_all_Cnumber_from_label
from tools import get_genuses
from tools import get_name


# In[31]:

import time
name = []
for genus in test:
    for Cn in test[genus]:
        time.sleep(5)
        name.append(get_genuses(Cn))
        print(Cn)
print(name)


# In[32]:

name


# In[37]:

if name[0][0].split()[0] in cag.ari:
    print("ari")
name[0][0].split()[0]


# In[38]:

for genus in test:
    Cnlist = test[genus]


# In[39]:

print(Cnlist)


# In[ ]:

i = 0
url = "http://rest.genome.jp/simcomp2/"
urlC = ""
for Cnumber in Clist:
    urlC += Cnumber + "+"
else:
    urlC = urlC[:-1]
url += urlC + "/" + urlC + "/cutoff=0.1"
urllib.request.urlretrieve(url, filename)


# In[40]:

import simnet2


# In[65]:

import importlib
simnet2 = importlib.reload(simnet2)


# In[43]:

simnet2.get_simcomp(Cnlist, "SIMCOMP2/Poaceae.txt")


# In[66]:

get_ipython().magic('matplotlib inline')
simnet2.make_graph(Cnlist, filepath="SIMCOMP2/Poaceae.txt")


# In[67]:

from tools import make_kcfs


# In[69]:

make_kcfs(Cnlist, "Poaceae/Oryza/only")


# In[76]:

path = "Poaceae/Oryza/only"
kosuu = dict()
with open(path + "splitedcount.txt")as f:
    units = f.read().split("\n")
    for unit in units[:-1]:
        temp = unit.split()
        kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])


# In[77]:

sorted(kosuu.items(), reverse=True, key=lambda x: x[1])


# In[80]:

path = "Poaceae/Oryza/only"
kosuu2 = dict()
with open(path + "kcfscount.txt")as f:
    units = f.read().split("\n")
    for unit in units[:-1]:
        temp = unit.split()
        kosuu2[(temp[1], temp[2])] = kosuu2.get((temp[1], temp[2]),0) + int(temp[3])


# In[82]:

sorted(kosuu2.items(), reverse=True, key=lambda x: x[1])


# In[72]:

len(Cnlist)


# In[84]:

al = search_all_Cnumber_from_label("C1x-C1z-C2b")


# In[85]:

print(len(al))


# In[ ]:



