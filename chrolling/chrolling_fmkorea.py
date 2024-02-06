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
class ChrollingFmkorea(ChrollingBase):
    '''
    fm-korea 크롤링하는 class
    
    
    '''
    url = 'https://www.fmkorea.com'
    
    def __init__(self):
        
        
        self.title_dic = dict()
        self.session = requests.Session()
        
        self.cookies: str = None
        self.last_cookies: str = None
        self.last_cookies_time: str = None 
        
        self.request_url = self.url + '/maple'
        self.last_url = self.request_url
        
        
        self.headers.update({'referer': self.last_url})
                    
        
        self.is_board_break = False
        self.max_page = 5
    
        self.site_name = 'fmkorea'
    
    

        
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
            request_url = self.request_url + f'&page={page}'
        
        response = requests.get(request_url, headers = self.headers, cookies = self.cookies)
            
        
        self.last_url = request_url
        return response

        
    def get_title_name(self, title):
        title = title.find("a")
        text = title.text.strip()
        href = title.get('href')
        
        return [text, href]
    
    def get_title_author(self, author):
        author_name = author.find('a').text
        
        author_score_str = author.find('img').get('title')
        start_idx = author_score_str.find('잉여력')
        last_idx = author_score_str.find('레벨')
        end_idx = author_score_str.find('/40')
        
        author_score = int(author_score_str[start_idx+4:last_idx-2])
        author_level = int(author_score_str[last_idx+3:end_idx])
        
        return [author_name, author_score, author_level]
    
    
        # 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
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
        soup = soup.find('tbody')
        titles = soup.findAll("td", attrs = {'class':['hotdeal_var8']})
        authors = soup.findAll("td", attrs = {'class':['author']})[4:]
        times = soup.findAll("td", attrs = {'class':['time']})[4:]
        views = soup.findAll("td", attrs = {'class':['m_no']})[8:]
        normal_views  = views[::2]
        recommend_views  = views[1::2]
        
        
        
        view_time = time.time()
        new_title_dic = dict()
        for title, author, time_text, n_view, r_view in zip(titles, authors, times, normal_views, recommend_views):
            new_dic = dict()
            
            title, href = self.get_title_name(title)
            href = self.url + href
            # if self.title_dic.get(href) !=None:
            #     self.is_board_break = True
            #     break
            
            new_dic['href'] = href
            new_dic['author'], new_dic['score'], new_dic['level'] = self.get_title_author(author)
            new_dic['time'] = time_text.text.strip()
            new_dic['title'] = title
            
            n_view = n_view.text.strip()
            r_view = r_view.text.strip()
            new_dic['normal_view'] = int(n_view) if n_view != '' else 0
            new_dic['reco_view'] = int(r_view) if r_view != '' else 0
            new_dic['view_time'] = view_time
            
            new_dic['site_name'] = self.site_name
            
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
                #self.cookies = None
                print(f'{page}번째에서 {self.site_name}가 우리를 배신했어 fucking {self.site_name}')
                break
            
            self.title_dic.update(self.parse_title(response))
            time.sleep(np.random.uniform(0,1))
    
    
    def chrolling_article(self):
        
        href_list = list(self.title_dic.keys())
        
        for href in href_list:
            
            board_url = href
            response = requests.get(board_url, headers = self.headers, cookies = self.cookies)
            
            
            html_text = response.text
            post_soup = bs(html_text, 'html.parser')

            article = post_soup.find("article").text
            times = post_soup.find('span', attrs = {'class':[ 'm_no']}).text

            self.title_dic[href]['article'] = article
            self.title_dic[href]['real_time'] = times
            
            random_value = np.random.uniform(0,self.max_sleep_time)
            time.sleep(random_value)
#%%



#%%
# ch = ChrollingFmkorea()
# #%%
# ch.max_page = 5
# ch.set_session(requests.Session())
# ch.chrolling_title()
# #ch.chrolling_article()
# #%%
# z = ch.title_dic
# #%%
# ch.cookies
# #%%



# values = ch.title_dic.values()
# old_str_list = list()
# old_str = ''
# old_len = 0

# for i, value in enumerate(values):
#     new_str = f'{i}.' + value['title'].strip() + '. '
#     new_len = len(new_str)
    
#     if old_len + new_len > 1000:
#         old_str_list.append(old_str)
#         old_str = ''
#         old_len = 0
#     else:
#         old_str += new_str
#         old_len +=new_len
#%%
'''
# 보드 전체 크롤링(현재 사용 X)
# '''
# board_data = pd.read_csv(f'{this_folder_dir}\\board_fmkorea.csv', encoding = 'cp949')
# board_href_list = list(board_data['href'])
# board_text_list = list(board_data['text'])
# title_dic = dict()

# # requests의 get함수를 이용해 해당 url로 부터 html이 담긴 자료를 받아옴

#%%
# for board_href in board_href_list:
#     board_url = ch.url + board_href
#     if title_dic.get(board_url) == None:
#         title_dic[board_url] = dict()
# #%%
# start_time = time.time()
# is_first = True
# for board_href, board_text in zip(board_href_list, board_text_list):
#     board_url = ch.url + board_href
#     last_url = ch.url + '/board'
#     now_url = board_url
    
#     board_dic = dict()
#     is_board_break = False
#     for page in range(1,3):
        
#         if is_first:
#             response = requests.get(now_url,
#                                 headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
#                                            ,'referer': last_url, 'language': "ko-KR"}
#                                             #, cookies = {'PHPSESSID': "j9ad5h5o391r90pnd6cbmv8d9v"}
#                                 )
#             cookie = response.cookies.items()[0][1]
#             is_first = False
#         else:
            
#             now_url = f"https://www.fmkorea.com/index.php?mid=football_korean&page={page}"
#             response = requests.get(now_url
#                                 , headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
#                                            ,'referer': last_url, 'language': "ko-KR"}
#                                 , cookies = {'PHPSESSID': cookie})
            
#         last_url = result_url
        
        
        
#     # 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
    
#         html_text = response.text
#         soup = bs(html_text, 'html.parser')
#         soup = soup.find('tbody')
#         titles = soup.findAll("td", attrs = {'class':['hotdeal_var8']})
#         authors = soup.findAll("td", attrs = {'class':['author']})[4:]
#         times = soup.findAll("td", attrs = {'class':['time']})[4:]
#         views = soup.findAll("td", attrs = {'class':['m_no']})[8:]
#         normal_views  = views[::2]
#         recommend_views  = views[1::2]
    
#         random_value = np.random.uniform(0,1)
#         time.sleep(random_value)
#         print(board_url, page, len(titles))
#         print(board_url, response.cookies)
    
    
    
#         view_time = time.time()
        
#         for title, author, time_text, n_view, r_view in zip(titles, authors, times, normal_views, recommend_views):
#             new_dic = dict()
            
#             title, href = get_title(title)
            
#             if title_dic[board_url].get(href) !=None:
#                 is_board_break = True
#                 break
            
#             new_dic['href'] = href
#             new_dic['author'], new_dic['score'], new_dic['level'] = get_author(author)
#             new_dic['time'] = time_text.text.strip()
#             new_dic['title'] = title
            
#             n_view = n_view.text.strip()
#             r_view = r_view.text.strip()
#             new_dic['n_view'] = int(n_view) if n_view != '' else 0
#             new_dic['r_view'] = int(r_view) if r_view != '' else 0
#             new_dic['view_time'] = view_time
            
            
#             board_dic[href] = new_dic
        
#         if is_board_break:
#             break
#     title_dic[board_url].update(board_dic)
#     random_value = np.random.uniform(0,3)
#     time.sleep(random_value)


#     print(board_url, time.time() - start_time)