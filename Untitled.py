
# coding: utf-8

# In[ ]:

import os


# In[ ]:

print(os.getcwd())


# In[ ]:

os.listdir()


# In[ ]:

os.mkdir("test2")


# In[ ]:

os.chdir("test2")


# In[ ]:

f = open('test.txt','a')

f.write('hoge\n')

f.close()


# In[ ]:

os.chdir("../")


# In[ ]:



