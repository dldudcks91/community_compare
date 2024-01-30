# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 20:43:11 2024

@author: user
"""














#%%
from elasticsearch import Elasticsearch

es = Elasticsearch('http://192.168.2.10:9200')
#%%
for i, value in enumerate(ch.title_dic.values()):
    print(i)
    es.index(index = 'dc', body = value)
#%%

es.indices.refresh(index = 'dc')
#%%
u = ch.title_dic
#%%
z = es.search(index= 'dc', body={'query':{'match':{'title':'오몽이'}}})
#%%

#%%
zz = z['hits']['hits']

#zzz = results['hits']['hits']
#%%
es.indices.delete(index='dc')