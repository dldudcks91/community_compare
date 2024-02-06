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
class ChrollingDC(ChrollingBase):
    
    url = 'https://gall.dcinside.com'
    def __init__(self):
        
        self.title_dic = dict()
        self.session = requests.Session()
        
        
        
        self.cookies = dict()
        self.phpsessid: int = None # dc에서 사용하는 쿠키
        self.csid: int = None # dc에서 사용하는 쿠키
        
        self.last_cookies: str = None
        self.last_cookies_time: str = None 
        
        self.request_url = self.url + "/board/lists/?id=maplestory_new"
        self.last_url = self.request_url
        
        self.headers.update({'referer': self.last_url})
                    
        
        
        self.is_board_break = False
        self.max_page = 5
    
        self.site_name = 'dc_inside'
        
    
    
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
        
        if not self.cookies:
            response = self.session.get(self.request_url, params = {'id': 'maplestory_new'}, headers = self.headers)
            
        else:
            
            self.request_url = f"https://gall.dcinside.com/board/lists/?id=maplestory_new&page={page}"
            response = self.session.get(self.request_url, 
                                    params = {'id': 'maplestory_new'},
                                    headers = self.headers,
                                    cookies = self.cookies)       
            
        return response

    
            
    def set_cookies(self):
        
        
            if self.cookies.get('PHPSESSID') != None:
                
                self.phpsessid = self.cookies['PHPSESSID']
            else:
                self.cookies['PHPSESSID'] = self.phpsessid if self.phpsessid != None else None
                
                
            if self.cookies.get('csid') != None:
                
                self.phpsessid = self.cookies['csid']
            else:
                self.cookies['csid'] = self.phpsessid if self.phpsessid != None else None
    
    
    def get_title_name(self, title):
        
        title = title.find("a")
        title_text = title.text.strip()
        href = title.get('href')
        
        return [title_text, href]
    
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
        
        titles = soup.findAll("td", attrs = {'class':['gall_tit']})[3:]
        authors = soup.findAll("td", attrs = {'class':['gall_writer']})[3:]
        times = soup.findAll("td", attrs = {'class':['gall_date']})[3:]
        normal_views = soup.findAll("td", attrs = {'class':['gall_count']})[3:]
        recommend_views  = soup.findAll("td", attrs = {'class':['gall_recommend']})[3:]
        
        
        
        view_time = time.time()
        new_title_dic=dict()
        for title, author, time_text, normal_view, recommend_view in zip(titles, authors, times, normal_views, recommend_views):
            
            new_dic = dict()
            
            title_text, href = self.get_title_name(title)
            href = self.url + href
            
            new_dic['title'] = title_text
            new_dic['href'] = href
            
            new_dic['author'] = author.text.strip()
            new_dic['normal_view'] = normal_view.text
            new_dic['reco_view'] = recommend_view.text
            
            new_dic['time'] = time_text.text
            new_dic['view_time'] = view_time
            new_title_dic[href] = new_dic
        
    
        return new_title_dic
    
    def chrolling_title(self):
        for i, page in enumerate(range(1,self.max_page+1)):
            response = self.request_title(page)
           
            if response.status_code == 200:
                self.cookies = response.cookies.get_dict()
                self.set_cookies()
                self.headers.update({'referer': self.request_url})
                print(f'{page}번째 page titles을 {self.site_name}가 성공적으로 내려주셨어')
            else:
                self.cookies = None #초심으로 돌아가버릐긔
                print(f'{i}번째에서 {self.site_name}가 우리를 배신했어 fucking {self.site_name}')
                break
            
            self.title_dic.update(self.parse_title(response))
            
            
            time.sleep(np.random.uniform(0,1))
    
#%%
from chrolling_fmkorea import ChrollingFmkorea
cf = ChrollingFmkorea()
cd = ChrollingDC()
#%%


from threading import Thread




cf.set_session(requests.Session())
cd.set_session(requests.Session())
#%%
cf.chrolling_title()



#%%
start_time = time.time()
threads = []

for i in [cf.chrolling_title, cd.chrolling_title]:
    
    thread = Thread(target = i)
    thread.start()

    threads.append(thread)

#cf.chrolling_title()
#cd.chrolling_title()


for thread in threads:
    thread.join()


end_time = time.time()
print(end_time - start_time)




#%%


# '''
# article 가져오기
# '''
# headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
           
#            , 'referer': "https://gall.dcinside.com/board/lists/?id=maplestory_new", 'language': "ko-KR"}

# href_list = list(title_dic.keys())

# i = 1
# cookies = {}
# for href in href_list:
    
#     board_url = href
#     response = session.get(board_url, headers = headers, cookies = cookies, params = {'id': 'maplestory_new'})
#     print(i, response.status_code, response.cookies.items())    
#     cookies = response.cookies.get_dict()
#     html_text = response.text
#     post_soup = bs(html_text, 'html.parser')

#     article = post_soup.find('div', attrs = {'class':[ 'write_div']})
    
#     article_text = article.text.strip()
    
#     images = article.findAll('img')
#     image_list = list()
    
#     for image in images:
#         image_list.append(image.get('src'))
    
    
#     time_text = post_soup.find('span', attrs = {'class':[ 'gall_date']}).text

#     title_dic[href]['article'] = article_text
#     title_dic[href]['real_time'] = time_text
#     title_dic[href]['image_list'] = image_list
    
#     random_value = np.random.uniform(0,1)
#     time.sleep(random_value)
    
    
      
#     i+=1