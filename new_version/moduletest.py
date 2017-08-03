
# coding: utf-8

# In[1]:

import Csearch # kcfsファイルをまとめたファイル(kcf)が同じディレクトリにあるとき
import nukidaC
import Csearch2 # 自分の環境専用
import kcfs2count 
import countersplit


# Csearchは全kcfsファイルがないとできない

# In[2]:

html = nukidaC.get_html("Klebsiella") # htmlオブジェクトを作る


# In[3]:

Clist = nukidaC.get_Cnumber(html, 1000) # htmlからCnumberを抜き出す


# In[4]:

print(len(Clist))


# In[5]:

Csearch2.search(Clist, "Klebsiella.kcfs") # kcfs束から必要なkcfsだけを抜き出す


# In[6]:

kcfs2count.kcfs2count("Klebsiella.kcfs", "Klebsiella.txt") # kcfs2countファイルを作る


# In[7]:

countersplit.split("Klebsiella.txt", "CKlebsiella.txt")
# countファイルのring, skeleton, inorganicのうちlimit(0)以上のものだけを取りだす


# Klebsiella属は数が少なすぎて共通構造を探すには不向き

# In[ ]:




# ストレプトマイセス属でテスト

# In[5]:

get_ipython().magic('time html = nukidaC.get_html("Streptomyces")')


# In[7]:

get_ipython().magic('time Clist = nukidaC.get_Cnumber(html, 2000)')


# In[9]:

print(len(Clist))


# In[11]:

get_ipython().magic('time Csearch2.search(Clist, "Streptomyces.kcfs")')


# In[12]:

get_ipython().magic('time kcfs2count.kcfs2count("Streptomyces.kcfs", "Streptomyces.txt")')


# In[13]:

get_ipython().magic('time countersplit.split("Streptomyces.txt", "splited_Streptomyces.txt")')


# In[ ]:



