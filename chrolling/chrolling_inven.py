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
class ChrollingInven(ChrollingBase):
    url = "https://www.inven.co.kr"
    
    def __init__(self):
        
        self.title_dic = dict()
        self.session = requests.Session()
        
        
        
        self.cookies = dict()
        self.phpsessid: int = None # dc에서 사용하는 쿠키
        self.csid: int = None # dc에서 사용하는 쿠키
        
        self.last_cookies: str = None
        self.last_cookies_time: str = None 
        
        self.request_url = self.url + "/board/maple/5974"
        self.last_url = self.request_url
        
        self.headers.update({'referer': self.last_url})
                    
        
        
        self.is_board_break = False
        self.max_page = 5
    
        self.site_name = 'inven'
        
        
    def request_title(self, page):
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
            request_url = self.request_url + f'?p={page}'
        response = self.session.get(request_url, 
                                    headers = self.headers,
                                    cookies = self.cookies)       
        
        self.last_url = request_url
        return response
        
        
    def get_title_name(self, title):
        title = title.find("a")
        text = title.text
        mid_idx = text.find(']')
        
        type_text = text[:mid_idx+1].strip()
        title_text = text[mid_idx+1:].strip()

        href = title.get('href')
        
        return [type_text, title_text, href]
        
    def parse_title(self, response):
        '''
        주어진 response 속 html을 parsing하는 함수
        
            
        Parameter
        ----------
        
            response: http get 요청 응답 결과
        
            
        Return
        -------
        
            new_title_dic: parsing결과를 dictionary로 반환. 추후 기존 dictionary에 update.
        '''
        html_text = response.text
        soup = bs(html_text, 'html.parser') 
        
        titles = soup.findAll("td", attrs = {'class':['tit']})[4:]
        authors = soup.findAll("td", attrs = {'class':['user']})[4:]
        times = soup.findAll("td", attrs = {'class':['date']})[4:]
        normal_views = soup.findAll("td", attrs = {'class':['view']})[4:]
        recommend_views  = soup.findAll("td", attrs = {'class':['reco']})[4:]
        
        view_time = time.time()
        new_title_dic=dict()
        for title, author, time_text, normal_view, recommend_view in zip(titles, authors, times, normal_views, recommend_views):
            
            new_dic = dict()
            
            type_text, title_text, href = self.get_title_name(title)
            
            new_dic['title_type'] = type_text
            new_dic['title'] = title_text
            new_dic['href'] = href
            
            new_dic['author'] = author.text.strip()
            new_dic['normal_view'] = normal_view.text
            new_dic['reco_view'] = recommend_view.text
            
            new_dic['time'] = time_text.text
            new_dic['view_time'] = view_time
            new_title_dic[href] = new_dic
        return new_title_dic
    
    def update_cookies(self, response):
        if response.cookies.get_dict() != None:
            
            self.cookies.update(response.cookies.get_dict())
            
            
    def chrolling_title(self):
        
        for i, page in enumerate(range(1,self.max_page+1)):
            response = self.request_title(page)
           
            if response.status_code == 200:
                self.update_cookies(response)
                self.headers.update({'referer': self.last_url})
                print(f'{page}번째 page titles을 {self.site_name}가 성공적으로 내려주셨어')
            else:
                #self.cookies = None #초심으로 돌아가버릐긔
                print(f'{page}번째에서 {self.site_name}가 우리를 배신했어 fucking {self.site_name}')
                break
            
            self.title_dic.update(self.parse_title(response))
            
            
            time.sleep(np.random.uniform(0,self.max_sleep_time))
    




#%%

#%%
# '''
# article 크롤링
# '''
# headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
#             , 'referer': "https://www.inven.co.kr/board/maple/5974", 'language': "ko-KR"}

# href_list = list(title_dic.keys())

# i = 1
# cookies = {}
# for href in href_list:
    
#     board_url = href
#     response = requests.get(board_url, headers = headers, cookies = cookies)
#     print(i, response.status_code, response.cookies.items())    
#     cookies = response.cookies.get_dict()
#     html_text = response.text
#     post_soup = bs(html_text, 'html.parser')

#     article = post_soup.find('div', attrs = {'id':[ 'powerbbsContent']})
    
#     article_text = article.text.strip()
    
#     images = article.findAll('img')
#     image_list = list()
    
#     for image in images:
#         image_list.append(image.get('src'))
    
    
#     time_text = post_soup.find('div', attrs = {'class':[ 'articleDate']}).text

#     title_dic[href]['article'] = article_text
#     title_dic[href]['real_time'] = time_text
#     title_dic[href]['image_list'] = image_list
    
#     random_value = np.random.uniform(0,1)
#     time.sleep(random_value)
    
    
      
#     i+=1
    
#%%

