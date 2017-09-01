
# coding: utf-8

# In[1]:

import urllib.request
import os
from classes import MCS_Finder
import time


# In[2]:

f = MCS_Finder("Streptomyces")


# In[3]:

get_ipython().magic('time f.make_kcfs(2000)')


# In[3]:

Clist = f.get_Cnlist_from_label2("C(C)-C(C)-C(C-C-C-C-C-C)-C-C-C-C-C-C-C-C-C")
print(Clist)


# In[31]:

get_ipython().run_cell_magic('time', '', 'i = 0\nfor Cnumber in Clist:\n    filepath = "SIMCOMP/" + Cnumber + ".txt"\n    if not os.path.exists(filepath):\n        url = "http://rest.genome.jp/simcomp/"+ Cnumber + "/knapsack"\n        i += 1\n        print(url, i)')


# In[23]:

url = "http://rest.genome.jp/simcomp/C00015228/knapsack"
filepath = "SIMCOMP/C00015228.txt"


# In[25]:

get_ipython().magic('time urllib.request.urlretrieve(url, filepath)')


# 約1分ぐらいかな?  
# sleepは3から5分ぐらいが妥当な気がする。

# In[30]:

get_ipython().run_cell_magic('time', '', 'i = 0\nt = time.time()\nfor Cnumber in Clist:\n    filepath = "SIMCOMP/" + Cnumber + ".txt"\n    if not os.path.exists(filepath):\n        url = "http://rest.genome.jp/simcomp/"+ Cnumber + "/knapsack"\n        urllib.request.urlretrieve(url, filepath)\n        i += 1\n        print(url, i)\n        print(time.time() - t)\n        print(time.strftime("%X"))\n        break\n        time.sleep(1200)\nprint("end")')


# In[6]:

time.localtime()


# In[8]:

time.strftime("%X")


# In[ ]:



