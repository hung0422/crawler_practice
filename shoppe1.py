import requests
import json
import random
import time
from urllib.parse import quote

def shoppe_search(keyword,page):
    '''
    搜尋商品資料存json檔
    :param keyword: 關鍵字
    :param page: 幾頁
    '''
    # 爬蟲設定
    ss = requests.session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'if-none-match-': '55b03-cfff720d86e83e9ebb9a71499ca182e0'
    }

    url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={}&limit=50&newest=0&order=desc&page_type=search&version=2'.format(keyword)
    writedata = {}

    # 要抓幾頁的資料
    for num in range(1,page+1):
        res = ss.get(url=url, headers=headers)
        data = json.loads(res.text)['items']
        for i in data:
            # name
            name = i['name']
            print('name:',name)
            # 最低價
            price_min = int(str(i['price_min'])[:-5])
            # 最高價
            price_max = int(str(i['price_max'])[:-5])
            # 售出數量
            historical_sold = i['historical_sold']
            # 評分
            item_rating = round(i['item_rating']['rating_star'],1)
            # 商品頁面
            shopid = i['shopid']
            itemid = i['itemid']
            # 轉url編碼
            encodename = quote(name)
            next = 'https://shopee.tw/' + '{}-i.{}.{}'.format(encodename,shopid,itemid)

            writedata[name] ={'最低價':price_min,'最高價':price_max,'售出數量':historical_sold,'評分':item_rating,'網址':next}

        # 隨機暫停 3~8 秒
        time.sleep(random.uniform(3, 8))
        url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={}&limit={}&newest=0&order=desc&page_type=search&version=2'.format(keyword,num*50)

    # 存json檔
    with open('{}.json'.format(keyword),'w',encoding='utf-8') as file:
        json.dump(writedata, file, ensure_ascii=False)

if __name__ == '__main__':
    shoppe_search(input('keyword:'),int(input('頁數:')))
