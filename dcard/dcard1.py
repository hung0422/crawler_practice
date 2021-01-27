import requests
import json
import random
import time
from bs4 import BeautifulSoup

def dcard_search(kanban):
    '''
    搜尋這個看板的所有文章
    :param kanban: 看板名稱
    :return: 看板的文章資料的list
    '''
    url = 'https://www.dcard.tw/service/api/v2/forums/{}/posts?popular=true&limit=30'.format(kanban)
    id = 0
    timelist = [2,3,6,8,9]
    datalist = []

    # 爬蟲設定
    ss = requests.session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    # 要抓幾頁的資料
    for i in range(1):
        res = ss.get(url=url, headers=headers)
        data = json.loads(res.text)
        for i in range(len(data)):
            if data[i]['excerpt'] == '':
                continue
            else:
                print(data[i]['title'])
                id = data[i]['id']
                # commentCount = data[i]['commentCount']
                datalist.append(dcard_detail(kanban,id))
                # datalist.append(dcard_message(id,commentCount))
        url = 'https://www.dcard.tw/service/api/v2/forums/{}/posts?popular=true&limit=30&before={}'.format(kanban,id)
        # 隨機暫停 2、3、6、8、9 秒
        randomsleep = random.choice(timelist)
        time.sleep(randomsleep)
    return datalist

def dcard_detail(kanban,id):
    '''
    抓文章的標題、日期等內容
    :param kanban: 看板名稱
    :param id: 文章id
    :return: 文章資訊
    '''
    url = 'https://www.dcard.tw/f/{}/p/{}'.format(kanban,id)
    # 爬蟲設定
    ss = requests.session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    res = ss.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 標題
    title = soup.select('div[class="sc-1eorkjw-1 kaykeD"]')[0].h1.text
    # 學校
    school = soup.select('div[class="s3d701-2 hjxRXj"]')[0].text
    # 日期
    write_date = soup.select('div[class="sc-1eorkjw-4 gVRLxG"]')[1].text
    # 文章內容
    content_data = soup.select('div[class="phqjxq-0 frrmdi"]')
    content_data2 = content_data[0].select('span')
    content = ''
    for i in content_data2:
        content += i.text.replace('\n','')

    # 隨機暫停 2~4 秒
    timelist2 = [2, 3, 4]
    randomsleep2 = random.choice(timelist2)
    time.sleep(randomsleep2)

    return kanban,title,school,write_date

def dcard_message(id,commentCount):
    '''
    將所有回應抓下來
    :param id: 文章id
    :param commentCount: 回應數
    :return: 所有回應
    '''
    num = 0
    message = ''
    # 爬蟲設定
    ss = requests.session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    while num < commentCount:

        url = 'https://www.dcard.tw/service/api/v2/posts/{}/comments?after={}'.format(id,num)

        res = ss.get(url=url, headers=headers)
        data = json.loads(res.text)

        for i in range(len(data)):
            try:
                message += data[i]['content'].replace('\n','')
            except KeyError:
                pass

        num += 30
    return message