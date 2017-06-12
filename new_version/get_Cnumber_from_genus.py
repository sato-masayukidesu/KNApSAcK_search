
# coding: utf-8

# In[1]:

import requests


# In[2]:

genus = input()
html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=" + genus)


# In[42]:

html.text


# In[15]:

import lxml.html


# In[39]:

dom = lxml.html.fromstring(html.text)


# In[40]:

print(dom)


# In[18]:

Cnumber = dom.xpath('//*[@id="tablekit-table-1"]/tbody/tr[2]/td[1]/a')[0].text


# In[107]:

print(dom.xpath('//*[@id="1143123"]/a[4]'))


# In[12]:

print(Cnumber)


# In[64]:

lxml.html.open_in_browser(dom)


# In[21]:

print("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=" + genus)


# In[23]:

print(html.text)


# In[111]:

Cnumber = dom.xpath('//*[@class="sortable d1"]/tr[4]/td[1]/a')


# In[112]:

print(Cnumber)


# In[81]:

IndexError


# In[115]:

i = 1
Cnumber = []
while(True):
    try:
        Cnumber.append(dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[1]/a')[0].text)
    except IndexError:
        print("shu-ryo-")
        break
    i += 1
    if i > 30:
        print("nagasugi")
        break


# In[116]:

print(Cnumber)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



