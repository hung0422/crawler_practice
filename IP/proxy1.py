import requests
import re
import json
import time
from bs4 import BeautifulSoup

start_time = time.time()

url = 'https://free-proxy-list.net/'

# 爬蟲設定
ss = requests.session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

res = ss.get(url=url, headers=headers)
# soup = BeautifulSoup(res.text, 'html.parser')
#
# data = soup.select('tr')
# https = []
# http = []
# for ip in data:
#     tds = ip.select('td')
#     if len(tds) == 8 :
#         if tds[6].text == 'yes':
#             https.append('https://'+ tds[0].text +':' +tds[1].text)
#         elif tds[6].text == 'no':
#             http.append('http://' + tds[0].text + ':' + tds[1].text)
#
# ipdict ={
#     'https':[],
#     'http':[]
#          }
#
# for ip in http:
#     try:
#         requests.get('https://api.ipify.org?format=json', proxies = {'http':ip, 'https':ip}, timeout = 5)
#         ipdict['http'].append(ip)
#         print('ok',ip)
#     except:
#         print('fail', ip)
#
# for ip in https:
#     try:
#         requests.get('https://api.ipify.org?format=json', proxies = {'http':ip, 'https':ip}, timeout = 5)
#         ipdict['https'].append(ip)
#         print('ok',ip)
#     except:
#         print('fail', ip)
#
#
# with open('ip.json', 'w', encoding='utf-8') as file:
#     file.write(json.dumps(ipdict))
#


allip = re.findall('\d+\.\d+\.\d+\.\d+:\d+', res.text)

ipdict = {'ip':[]}

for ip in allip:
    try:
        requests.get('https://api.ipify.org?format=json', proxies={'http': ip, 'https': ip}, timeout=5)
        ipdict['ip'].append(ip)
        print('ok', ip)
    except:
        print('fail', ip)

with open('ip2.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(ipdict))
end_time = time.time()
print('幾秒',end_time-start_time)