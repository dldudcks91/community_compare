# requests 패키지 가져오기
import requests               
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd


import sys
import os
import time
'''

'''
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
            , 'language': "ko-KR"}

cookies = dict()
phpsessid = None
csid = None


#%%
response = requests.get("https://gall.dcinside.com/board/lists/?id=maplestory_new", 
                        params = {'id': 'maplestory_new'}, 
                        headers = headers,
                        cookies = cookies
            )
cookies = response.cookies.get_dict()
print(response.status_code)
html_text = response.text

soup = bs(html_text, 'html.parser')
#%%
cookies = response.cookies.get_dict()

if cookies.get('PHPSESSID') == None:
    if phpsessid == None:
        pass
    else:
        cookies['PHPSESSID'] = phpsessid
else:
    
    phpsessid = cookies['PHPSESSID']
if cookies.get('csid') == None:
    if csid == None:
        pass
    else:
        cookies['csid'] = csid
else:
    csid = cookies['csid']
    
#%%

#%%
def get_title_name(title):
    
    title = title.find("a")
    title_text = title.text.strip()
    href = title.get('href')
    
    return [title_text, href]
#%%

titles = soup.findAll("td", attrs = {'class':['gall_tit']})[3:]
authors = soup.findAll("td", attrs = {'class':['gall_writer']})[3:]
times = soup.findAll("td", attrs = {'class':['gall_date']})[3:]
normal_views = soup.findAll("td", attrs = {'class':['gall_count']})[3:]
recommend_views  = soup.findAll("td", attrs = {'class':['gall_recommend']})[3:]

view_time = time.time()
new_title_dic=dict()
for title, author, time_text, normal_view, recommend_view in zip(titles, authors, times, normal_views, recommend_views):
    
    new_dic = dict()
    
    title_text, href = get_title_name(title)
    
    new_dic['title'] = title_text
    new_dic['href'] = href
    
    new_dic['author'] = author.text.strip()
    new_dic['normal_view'] = normal_view.text
    new_dic['reco_view'] = recommend_view.text
    
    new_dic['time'] = time_text.text
    new_dic['view_time'] = view_time
    new_title_dic[href] = new_dic
#%%
