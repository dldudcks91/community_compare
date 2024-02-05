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

