import sys
import requests
import json
client_id = "xpcudfyxf2"
client_secret = "oq6nCL6ck7vcjGHy7JdwF2XDp14pWlkjuoyQTnDj"
url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}
content = old_str_list[4]
data = {
  "content": content
}
print(json.dumps(data, indent=4, sort_keys=True))
response = requests.post(url, data=json.dumps(data), headers=headers)
rescode = response.status_code
if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)
    
#%%
z = response.text
    
#%%

zz = eval(z)
#%%
zzz = zz['sentences']
zzzz = sorted(zzz, key = lambda x: x['confidence']['negative'], reverse = True)