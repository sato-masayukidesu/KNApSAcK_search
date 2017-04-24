
# coding: utf-8

# In[1]:

import urllib.request


# In[16]:

x = input()
url = "http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=%s" % (x)


# In[17]:

print(url)


# In[18]:

urllib.request.urlretrieve(url, '%s.txt' % (x))


# In[23]:

ld = open("%s.txt" % (x))
lines = ld.readlines()
ld.close()

for line in lines:
    if line.find("word=C") >= 0:
        print(line[49:-34])
        urllib.request.urlretrieve("http://knapsack3d.sakura.ne.jp/mol3d/%s.3d.mol" % (line[49:-34]), '%s.mol' % (line[49:-34]))


# In[ ]:



