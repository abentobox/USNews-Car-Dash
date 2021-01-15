#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 02:21:18 2021

@author: Andrew
"""

#%%
#!pip install os
#import os
import requests
from lxml import html
import pandas as pd
import json as json

#%%
with open(("/Users/Andrew/Documents/Python Projects/USNews Cars/Data/Browse.json")) as f:
    data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
#mydata = pd.DataFrame(data)
# var = mydata["models"][0]
# var = var[0]
# sub = pd.DataFrame(var)
# sub2 = sub["years"][0]
# (data[0]["models"][0]["years"][0]["year"])
#%%

print(data["data"]["listings"])

#%% Start with web pull
website_url = 'https://cars.usnews.com/ajax/car-finder/browse?sort=alpha&page=1'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
response = requests.get(website_url,headers=headers)

page = response.text
#%%
with open(("/Users/Andrew/Documents/Python Projects/USNews Cars/Data/Browse.json")) as f:
    page = f.read()
s = page.find('[{"trims"')
e = page.find(',"bread')
substr = page[s:e]

#page = html.fromstring(page)

# parse strings to list
null = None
false = False
true = True
listings = eval(substr)


#%% Jonathan Hsu flatten function
# Source: https://medium.com/better-programming/how-to-flatten-a-dictionary-with-nested-lists-and-dictionaries-in-python-524fd236365

import collections
def flatten(d, sep="_"):


    obj = collections.OrderedDict()

    def recurse(t, parent_key=""):
        
        if isinstance(t,list):
            for i in range(len(t)):
                recurse(t[i],parent_key + sep + str(i) if parent_key else str(i))
        elif isinstance(t,dict):
            for k,v in t.items():
                recurse(v,parent_key + sep + k if parent_key else k)
        else:
            obj[parent_key] = t

    recurse(d)

    return obj


#%% Pandas exploded
listings = eval(substr)
expdf = pd.DataFrame(listings)

# Rename columns with unclear names

expdf = expdf.rename(columns = {'name': 'year_make_model','chrome_id':'base_id'})


# Explode product ranking column
pranktemp = expdf['product_ranking'].apply(pd.Series)
expdf = pd.concat([expdf.drop(['product_ranking'], axis=1), pranktemp], axis=1) 
pranktemp = expdf['category'].apply(pd.Series)
pranktemp = pranktemp.drop(columns = [0,'description'], axis = 1)
pranktemp = pranktemp.rename(columns = {'name':'ranking_name'})
expdf = pd.concat([expdf.drop(['category'], axis=1), pranktemp], axis=1) 

# Explode trims column
expdf = expdf.explode('trims')
explodedtemp = expdf['trims'].apply(pd.Series)
#basetrimlist = expdf[['chrome_id','make' ]]
#basetrimlist = basetrimlist.assign(make = 1)
#basetrimlist = basetrimlist.rename(columns = {'make':'baseflag'})
#explodedtemp = explodedtemp.merge(basetrimlist, on = 'chrome_id', how = 'outer')
expdf = pd.concat([expdf.drop(['trims'], axis=1), explodedtemp], axis=1)
expdf['baseflag'] = 0
expdf.loc[expdf['base_id'] == expdf['chrome_id'], 'baseflag'] = True 
#%%
listings = eval(substr)
expdf = pd.DataFrame(listings)
expdf2 = expdf.explode('trims')
explodedtemp = expdf2['trims'].apply(pd.Series)
expdf = expdf.drop(['trims'], axis=1)
join = expdf.join(explodedtemp, rsuffix="_right") 

#%% identify base model
listings = eval(substr)
expdf = pd.DataFrame(listings)
expdf2 = expdf.explode('trims')
explodedtemp = expdf2['trims'].apply(pd.Series)
#%%





