# requests 패키지 가져오기
import requests               
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd


import sys
import os
import time

this_folder_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(this_folder_dir)
from chrolling_base import ChrollingBase
#%%


class ChrollingMapleCafe():
    url = "https://cafe.naver.com/black3vezx"
    
    def __init__(self):
        
        self.title_dic = dict()
        self.session = requests.Session()
        
        
        
        self.cookies = dict()
        self.phpsessid: int = None # dc에서 사용하는 쿠키
        self.csid: int = None # dc에서 사용하는 쿠키
        
        self.last_cookies: str = None
        self.last_cookies_time: str = None 
        
        self.request_url = self.url + '/ArticleList.nhn?search.clubid=28957699&amp;search.boardtype=L'
        self.last_url = self.request_url
        
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        self.headers.update({'referers': self.url})
                    
        
        
        self.is_board_break = False
        self.max_page = 5
    
        self.site_name = 'inven'
        
    def request_title(self, page, url = None):
        '''
        게시판 title response가져오는 함수
        
            cookies 존재 유무에 따라 요청하는 url이 바뀜
        
        Parameter
        ----------
        
            page: 게시판 page
        
            
        Return
        -------
        
            reponse: http get 요청 결과 response
        '''
        
        
            
        
            
            
    
        if page == 1:
            request_url =  self.request_url
        else:
            request_url = url
        response = self.session.get(request_url, headers = self.headers, cookies = self.cookies)       
        
        self.last_url = request_url
        return response
        


#%%
cmf = ChrollingMapleCafe() 
https://cafe.naver.com/black3vezx?iframe_url=/ArticleList.nhn%3Fsearch.clubid=28957699%26search.boardtype=L%26search.totalCount=151%26search.cafeId=28957699%26search.page=2
#%%
response = cmf.request_title(1)

cmf.headers.update({'referers': cmf.request_url})
#%%
cmf.headers
#%%

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
    href = cmf.url + href
    new_dic['title_type'] = type_text
    new_dic['title'] = title_text
    new_dic['href'] = href
    
    new_dic['author'] = author.text.strip()
    new_dic['normal_view'] = normal_view.text
    
    
    new_dic['time'] = time_text.text
    new_dic['view_time'] = view_time
    new_title_dic[href] = new_dic