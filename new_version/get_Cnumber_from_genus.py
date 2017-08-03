
# coding: utf-8

# In[ ]:

import requests


# In[ ]:

genus = input()
html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=" + genus)


# In[ ]:

html.text


# In[ ]:

import lxml.html


# In[ ]:

dom = lxml.html.fromstring(html.text)


# In[ ]:

print(dom)


# In[ ]:

Cnumber = dom.xpath('//*[@id="tablekit-table-1"]/tbody/tr[2]/td[1]/a')[0].text


# In[ ]:

print(dom.xpath('//*[@id="1143123"]/a[4]'))


# In[ ]:

print(Cnumber)


# In[ ]:

lxml.html.open_in_browser(dom)


# In[ ]:

print("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=" + genus)


# In[ ]:

print(html.text)


# In[ ]:

Cnumber = dom.xpath('//*[@class="sortable d1"]/tr[4]/td[1]/a')


# In[ ]:

print(Cnumber)


# In[ ]:

IndexError


# In[ ]:

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


# In[ ]:

print(Cnumber)


# In[ ]:




# In[ ]:

html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=C00000995")


# In[ ]:

dom = lxml.html.fromstring(html.text)


# In[ ]:

print(html.text)


# In[ ]:

genus = dom.xpath('//*[@class="sortable d1"]/tr[1]/td[6]')[0].text


# In[ ]:

print(genus)


# In[ ]:

genus.split()[0].lower()


# In[ ]:

html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word=citrus")


# In[ ]:

dom = lxml.html.fromstring(html.text)


# In[ ]:

i = 1
Cnumber = []
while(True):
    try:
        if "Citrus" != dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[6]/font')[0].text.split()[0]:
            print(dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[1]/a')[0].text)
    except IndexError:
        print("shu-ryo-")
        print(i)
        break
    i += 1
    if i > 1000:
        print("nagasugi")
        break


# In[ ]:



