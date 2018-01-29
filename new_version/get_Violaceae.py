
# coding: utf-8

# In[1]:

import lxml.html
import requests
import os
family = "Violaceae"
if not os.path.exists(family):
    os.mkdir(family)


# In[2]:

html = requests.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=" + family + "&lvl=5")


# In[3]:

print(html)


# In[4]:

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

print(ci)


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

print(len(genuses))


# In[11]:

spe = dom.xpath('//*[@title="species"]/strong')


# In[12]:

print(len(spe))


# In[13]:

genlist = []
for genus in genuses:
    genlist.append(genus.text)
print(len(genlist))


# In[14]:

import pickle
with open(family + "/genuses.pickle", "wb")as fi:
    pickle.dump(genlist, fi)


# In[15]:

with open(family + "/genuses.pickle", "rb")as fi:
    genlist2 = pickle.load(fi)
print(genlist == genlist2)


# In[16]:

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


# In[ ]:




# In[1]:

from classes2 import control_all_genus


# In[2]:

cag = control_all_genus("Violaceae")


# In[3]:

cag.ari


# In[4]:

sorted(cag.get_number_of_Cnumber().items(), reverse = True, key =lambda x: x[1]) 


# In[5]:

sorted(cag.get_split_kcfs().items(), reverse=True, key=lambda x: x[1])


# In[6]:

specific = cag.get_specifics()
s = sorted(specific.items(), reverse=True, key=lambda x: x[1])
s


# やっぱ2属しかないから無理そう

# In[8]:

glen = []
for genus in cag.ari:
    with open("Violaceae/" + genus + "/kcfs.kcfs")as f:
        Cnlist = []
        molecule = f.read().split("///\n")
        for mol in molecule[:-1]:
            Cn = mol.split("\n")[0].split()[1]
            Cnlist.append(Cn)
        glen.append((genus, len(Cnlist)))
sorted(glen, reverse=True, key=lambda x: x[1])


# In[ ]:



