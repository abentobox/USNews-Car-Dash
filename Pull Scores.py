#!/usr/bin/env python
# coding: utf-8

# # USNews Data Scrape

# ### Step 1. Load Required Python Packages

# In[41]:


#!pip install requests
#!pip install lxml
#!pip install pandas

import requests
from lxml import html
import pandas as pd
import numpy as np


# ### Step 2. Make A Call To Website

# In[66]:


modeldf = pd.read_csv("USNews Models and Years.csv")
urllist = modeldf["Url"]
makelist = modeldf["Make"]
modlist = modeldf["Model"]
yearlist = modeldf["Year"]


i=0


# In[98]:



masterdf = pd.DataFrame(columns  = ['Make', 'Model', 'Year','Segment','Price Range' ,"Critics' Rating",'Performance','Interior', 'Total Cost of Ownership','Safety','Reliability','Overall'])

for i in range(0, len(urllist)):

    website_url = 'https://cars.usnews.com' + urllist[i]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    response = requests.get(website_url,headers=headers)

    e = html.fromstring(response.text)
    
    segment1=e.xpath('//a[@class = "vwo-rankings-awards-link"]/text()')

    column_headers = e.xpath('//table[1]/tbody/tr/td[1]/text()')
    column_headers = column_headers + ["Reliability","Overall","Make", "Model", "Year", "Segment", 'Price Range']
    column_headers = [x.replace('\n', '') for x in column_headers]
    column_headers = [x.replace('  ', '') for x in column_headers]
    column_headers = [x.replace(':', '') for x in column_headers]
    
    values = e.xpath('//table[1]/tbody/tr/td[@class="float-right item scorecard__value-label"]/text()')
    overall = e.xpath('//p[@class = "scorecard__score"]/text()')
    reliability = e.xpath('//td/a/div[@class = "reliability float-left"]/@alt')
    if not reliability:
        reliability = ['']
    
#Grab segment data
    segment = e.xpath('//a[@class = "vwo-rankings-awards-link"]/text()')
    segment = list(dict.fromkeys(segment))
    segment = [x.replace(str(yearlist[i])+' ', '') for x in segment] 
    prange = [x for x in segment if "Used" in x]
    segment = [x for x in segment if "Used" not in x]
    
    values = values + reliability + overall + [makelist[i], modlist[i]]
    values = [x.replace('\n', '') for x in values]
    values = [x.replace('  ', '') for x in values]
    values = [x.replace(':', '') for x in values]
    values = [x.replace('TBD', '') for x in values]
    values.append(yearlist[i])
    values.append(segment)
    values.append(prange)
    values = [values]
    
    #print(column_headers)
    #print(values)
    
    tempdf = pd.DataFrame(values, columns = column_headers)
    masterdf = masterdf.append(tempdf)


# ### Step 3. Scrape Table Headers From Website

# In[99]:


masterdf.to_csv('output w segment.csv')


# ### Create unique list of segments

# In[]
seglist = masterdf["Segment"]
seglist = seglist.reset_index(drop=True)
i = 0
seglistmaster = []
for i in range(0,len(seglist)):
    value = seglist.iloc[i]
    value = value.replace("[", "")
    value = value.replace("]", "")
    value = value.replace("'", "")
    seglist.iloc[i] = value
    value = list(value.split("', '"))
    seglistmaster.extend(value)
    i+=1
   
seglistmaster = list(dict.fromkeys(seglistmaster))
seglistmaster = sorted(seglistmaster, key=str.lower)
   
 # In[]

prangelist = masterdf["Price Range"]
prangelist = prangelist.reset_index(drop=True)
i = 0
prangelistmaster = []
for i in range(0,len(prangelist)):
    value = prangelist.iloc[i]
    prangelist[i] = ', '.join(value)
    prangelistmaster.extend(value)
    i+=1
  
prangelistmaster = list(dict.fromkeys(prangelistmaster))
prangelistmaster = sorted(prangelistmaster, key=str.lower)

# In[]
segdf = pd.DataFrame(seglistmaster)
prangedf = pd.DataFrame(prangelistmaster) 
segdf.to_csv('segment list clean.csv')
prangedf.to_csv('price range list clean.csv')

# In[]
masterdf["Segment_clean"] = list(seglist)
masterdf["Price Range_clean"] = list(prangelist)
masterdf.to_csv('output w segment2.csv')

