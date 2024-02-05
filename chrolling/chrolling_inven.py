# requests 패키지 가져오기
import requests               
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd


import sys
import os
import time
'''
인벤은 특정시간내에 몇회이상 크롤링을 하면 못 가져가게 만드는거 같음
'''
#from chrolling_base import ChrollingBase

class ChrollingInven():
    url = "https://www.inven.co.kr"
session = requests.Session()
response = session.get("https://www.inven.co.kr/board/maple/5974")
cookies = response.cookies.items()[0][1]
print(response.status_code)
html_text = response.text

soup = bs(html_text, 'html.parser')
#%%
cookies = response.cookies.get_dict()
#%%
def get_title_name( title):
    title = title.find("a")
    text = title.text
    mid_idx = text.find(']')
    
    type_text = text[:mid_idx+1].strip()
    title_text = text[mid_idx+1:].strip()

    href = title.get('href')
    
    return [type_text, title_text, href]
#%%


titles = soup.findAll("td", attrs = {'class':['tit']})[4:]
authors = soup.findAll("td", attrs = {'class':['user']})[4:]
times = soup.findAll("td", attrs = {'class':['date']})[4:]
normal_views = soup.findAll("td", attrs = {'class':['view']})[4:]
recommend_views  = soup.findAll("td", attrs = {'class':['reco']})[4:]
#%%
view_time = time.time()
new_title_dic=dict()
for title, author, time_text, normal_view, recommend_view in zip(titles, authors, times, normal_views, recommend_views):
    
    new_dic = dict()
    
    type_text, title_text, href = get_title_name(title)
    
    new_dic['title_type'] = type_text
    new_dic['title'] = title_text
    new_dic['href'] = href
    
    new_dic['author'] = author.text.strip()
    new_dic['normal_view'] = normal_view.text
    new_dic['reco_view'] = recommend_view.text
    
    new_dic['time'] = time_text.text
    new_dic['view_time'] = view_time
    new_title_dic[href] = new_dic

#%%
title_dic = dict()
title_dic.update(new_title_dic)
#%%

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
            , 'referer': "https://www.inven.co.kr/board/maple/5974", 'language': "ko-KR"}

href_list = list(title_dic.keys())

i = 1
cookies = {}
for href in href_list:
    
    board_url = href
    response = requests.get(board_url, headers = headers, cookies = cookies)
    print(i, response.status_code, response.cookies.items())    
    cookies = response.cookies.get_dict()
    html_text = response.text
    post_soup = bs(html_text, 'html.parser')

    article = post_soup.find('div', attrs = {'id':[ 'powerbbsContent']})
    
    article_text = article.text.strip()
    
    images = article.findAll('img')
    image_list = list()
    
    for image in images:
        image_list.append(image.get('src'))
    
    
    time_text = post_soup.find('div', attrs = {'class':[ 'articleDate']}).text

    title_dic[href]['article'] = article_text
    title_dic[href]['real_time'] = time_text
    title_dic[href]['image_list'] = image_list
    
    random_value = np.random.uniform(0,1)
    time.sleep(random_value)
    
    
      
    i+=1
    
#%%

