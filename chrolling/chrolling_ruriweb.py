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
           , 'referers': 'https://cafe.naver.com/black3vezx/'
           , 'language': "ko-KR"}

cookies = dict()
phpsessid = None
csid = None

url = 'https://cafe.naver.com/black3vezx/ArticleList.nhn?search.clubid=28957699&amp;search.boardtype=L'
#%%

session = requests.Session()
#%%
response = session.get(url, 
                        
                        headers = headers,
                        cookies = cookies
            )
cookies = response.cookies.get_dict()
print(response.status_code)
html_text = response.text

soup = bs(html_text, 'html.parser')
#%%
#types = soup.findAll("a", attrs = {'class':['link_name']})[6:]
titles = soup.findAll("td", attrs = {'class':['td_article']})[6:]
authors = soup.findAll("td", attrs = {'class':['td_name']})[6:]
times = soup.findAll("td", attrs = {'class':['td_date']})[6:]
normal_views = soup.findAll("td", attrs = {'class':['td_view']})[6:]

#%%

def get_title_name(title):
    
    type_html, title_html, *comment_html = title.findAll("a")
    type_text = type_html.text.strip()
    title_text = title_html.text.strip()
    href = title_html.get('href')
    
    return [type_text, title_text, href]

#%%

#%%
view_time = time.time()
new_title_dic=dict()
for title, author, time_text, normal_view in zip(titles, authors, times, normal_views):
    
    new_dic = dict()
    
    type_text, title_text, href = get_title_name(title)
    href = url + href
    new_dic['title_type'] = type_text
    new_dic['title'] = title_text
    new_dic['href'] = href
    
    new_dic['author'] = author.text.strip()
    new_dic['normal_view'] = normal_view.text
    
    
    new_dic['time'] = time_text.text
    new_dic['view_time'] = view_time
    new_title_dic[href] = new_dic