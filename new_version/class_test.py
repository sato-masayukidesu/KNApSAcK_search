
# coding: utf-8

# In[1]:

from classes import MCS_Finder


# In[2]:

f = MCS_Finder("Streptomyces")


# In[3]:

get_ipython().magic('time f.make_kcfs(2000)')


# In[3]:

get_ipython().magic('time f.make_image(label="C8x-N4y-C8y-C8y-N5x")')


# In[3]:

get_ipython().magic('time f.make_image("C(C)-C(C)-C(C-C-C-C-C-C)-C-C-C-C-C-C-C-C-C")')


# In[7]:

Cnlist = f.get_Cnlist_from_label("C8x-N4y-C8y-N5x-C8x-N5x-C8y-C8y-N5x")


# In[8]:

print(Cnlist)


# In[9]:

print(len(Cnlist))


# In[4]:

print(len(f.mol_list))


# In[6]:

from counter_search import counter_search2
import re


# In[6]:

f.mollist = None
Cnlist = counter_search2(f.gene, "C8x-N4y-C8y-N5x-C8x-N5x-C8y-C8y-N5x")
f.get_molfile(Cnlist)
f.find_MCS(Cnlist)
f.find_MCS_grid_image(Cnlist)


# In[14]:

print(f.mollist)
print(Cnlist)


# In[7]:

f.get_Cnlist_from_label2("C(C)-C(C)-C(C-C-C-C-C-C)-C-C-C-C-C-C-C-C-C")


# In[ ]:



