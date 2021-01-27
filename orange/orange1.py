'''
爬取TechOrange每天的文章
'''
import os
import time
import datetime
import random
import json
import requests
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup

# 爬蟲設定
ss = requests.session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

# 設定資料夾
folder = r'./orange_data'
if not os.path.exists(folder):
    os.mkdir(folder)

# 開啟瀏覽器
driver = Chrome('../chromedriver')
url = 'https://buzzorange.com/techorange/'
driver.get(url)

# 已經抓過的文章存這裡,避免重複爬取
title_list = []
# 瀏覽器滾動條
js="var action=document.documentElement.scrollTop=5000"

def nowtime():
    # 今天日期
    locTime = datetime.datetime.now()
    strtime =locTime.strftime('%Y/%m/%d')
    return strtime

def get_tiltetime(i):
    tiltetime = i.find_element_by_tag_name('time').text
    return tiltetime

def get_titlespan(i):
    titlespan = i.find_element_by_tag_name('span').text
    return titlespan

def get_url(i):
    # 抓取文章url
    url = i.find_element_by_tag_name('a').get_attribute('href')
    return url

def get_data(url):
    # 抓取文章相關內容
    res = ss.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = get_title(soup)
    content = get_content(soup)
    date = get_date(soup)
    data_json = {
        'title':title,
        'date':date,
        'content':content
                 }
    write_json(data_json)

def get_title(soup):
    # 抓取文章標題
    title = soup.select('h1[class="entry-title"]')[0].text
    return title

def get_content(soup):
    # 抓取文章內容
    detail = soup.select('div.fb-quotable p')
    detail2 = ''
    for i in detail:
        detail2 += i.text
    return detail2

def get_date(soup):
    # 抓取文章發布時間
    date = soup.select('div.article-post-date time')[0].text
    return date

def write_json(data_json):
    # 寫入json檔
    title_data = data_json.get('title')
    try:
        with open(folder + '/{}.json'.format(title_data), 'w', encoding='utf-8') as f:
            json.dump(data_json, f, ensure_ascii=False)
            print('done!')
    except FileNotFoundError:
        with open(folder + '/{}.json'.format(title_data.replace('/', '-')), 'w', encoding='utf-8') as f:
            json.dump(data_json, f, ensure_ascii=False)
            print('done!')
    except:
        pass

def get_orange():
    page = 0
    while page != 1000:
        title = driver.find_elements_by_class_name('entry-header')
        if page == 0:
            for i in title:
                tiltetime = get_tiltetime(i)
                titlespan = get_titlespan(i)
                url = get_url(i)
                # 抓取包含至頂的今日文章
                if titlespan == '本日聚焦':
                    get_data(url)
                    time.sleep(random.uniform(5, 10))
                elif tiltetime == nowtime():
                    get_data(url)
                    title_list.append(i.text)
                    time.sleep(random.uniform(5,10))
                # 如果已經沒有今天的文章就結束
                else:
                    page = 999
                    break
            page += 1
            # 滾動瀏覽器(下一頁)
            driver.execute_script(js)
        else:
            for i in title:
                tiltetime = get_tiltetime(i)
                titlespan = get_titlespan(i)
                url = get_url(i)
                # 抓取還沒抓完的今日文章
                if titlespan == '本日聚焦' or i.text in title_list:
                    pass
                elif tiltetime == nowtime() and i.text not in title_list:
                    get_data(url)
                    title_list.append(i.text)
                    time.sleep(random.uniform(5, 10))
                # 如果已經沒有今天的文章就結束
                else:
                    page = 999
                    break
            page += 1
            # 滾動瀏覽器(下一頁)
            driver.execute_script(js)
    # 關閉視窗
    driver.quit()

if __name__ == '__main__':
    get_orange()