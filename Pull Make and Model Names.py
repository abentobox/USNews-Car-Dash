#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from lxml import html
import pandas as pd


# In[15]:



website_url = 'https://cars.usnews.com/cars-trucks'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
response = requests.get(website_url,headers=headers)
page = html.fromstring(response.text)
text = page.xpath('//ul[@class = "List__ListWrap-rhf5no-0 ftdxlE Homepage__BrandList-sc-1t17kte-6 jgspEN"]/li[@class="List__ListItem-rhf5no-1 hPJeDU"]/a/text()')
text


# In[126]:


#!pip install os
#import os
import json

with open(os.path.expanduser("~/Desktop/usnews full make model list.json")) as f:
    data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
mydata = pd.DataFrame(data)
var = mydata["models"][0]
var = var[0]
sub = pd.DataFrame(var)
sub2 = sub["years"][0]
(data[0]["models"][0]["years"][0]["year"])


# In[131]:


i=0
j=0
k=0
arr = []
for i in range(0, len(data)):
    thismake = data[i]["models"]
    mymake = data[i]["make"]
    for j in range(0, len(thismake)-1):
        thismodel = thismake[j]["years"]
        mymodel = thismake[j]["model"]
        for k in range(0, len(thismodel)-1):
            thisyear = thismodel[k]
            myyear = thisyear["year"]
            myurl = thisyear["url"]
            temp = [mymake,mymodel,myyear,myurl]
            arr.append(temp)
        k+=1
    j+=1
i+=1
        
mydf = pd.DataFrame(arr, columns = ["Make","Model","Year","Url"])
mydf


# In[132]:


mydf.to_csv("USNews Models and Years.csv")


# In[ ]:




