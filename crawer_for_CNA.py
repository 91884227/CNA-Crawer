#!/usr/bin/env python
# coding: utf-8

# # import tool

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from itertools import chain


# In[2]:


def get_all_url():
    url = "https://www.cna.com.tw/list/aall.aspx"
    my_headers =  {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
    r = requests.get(url, headers = my_headers)
    soup =  BeautifulSoup(r.text)
    all_url = [i.get("href") for i in soup.select(".first-level")]
    all_url = [i for i in all_url if i.startswith("https://www.cna.com.tw/")] # 初步篩選網址
    return(all_url)


# In[3]:


def url_get_data(url_):
    try:
        my_headers =  {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
        r = requests.get(url_, headers = my_headers)
        soup =  BeautifulSoup(r.text) 
        #buf = [i.next.next.text for i in soup.select(".listInfo")]
        buf = [i.next.text for i in soup.select(".listInfo")]
        return(buf)
    except:
        print("error happand in %s" % url_)


# In[4]:


def output_data(buf_):
    df = pd.DataFrame(buf_)
    df.columns = ["title"]
    name = "CNA_title.csv"
    df.to_csv(name, index = False, encoding= 'UTF-8')


# In[7]:


if __name__ == '__main__':
    list_URL = get_all_url()
    buf = [ url_get_data(i) for i in tqdm(list_URL)]
    buf_1d = list(chain.from_iterable(buf))
    try:
        output_data(buf_1d)
        print("success to create file CNA_title.csv")
    except:
        print("fail to create file")  

