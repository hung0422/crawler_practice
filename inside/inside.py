'''
爬取INSIDE的文章
'''
import requests
import json
import os
import time
import random
from bs4 import BeautifulSoup

# 爬蟲設定
ss = requests.session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

def newfolder(keyword:str):
    # 設定資料夾
    folder = r'./{}/'.format(keyword)
    return folder

def creatfolder(folder):
    # 創建資料夾
    folder = newfolder(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)

def url_soup(url):
    # 爬取網頁
    res = ss.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def get_data(url):
    # 抓取文章相關內容
    soup = url_soup(url)
    title = get_title(soup)
    date = get_essaydate(soup)
    intro = get_introduction(soup)
    content = get_content(soup)

    data_json = {
        'title':title,
        'date':date,
        'intro':intro,
        'content':content
    }
    write_json(data_json)

def get_title(soup):
    # 抓取文章標題
    title = soup.select('h1[class="post_header_title js-auto_break_title"]')[0].text
    return title

def get_essaydate(soup):
    # 抓取文章發布時間
    date = soup.select('li[class="post_date"]')[0].text
    date = date.strip()
    return date

def get_introduction(soup):
    # 抓取文章開頭簡介
    try:
        intro = soup.select('div[class="post_introduction"]')[0].text
        intro = intro.strip()
    except IndexError :
        intro = ''
    return intro

def get_content(soup):
    # 抓取文章內容
    content = soup.select('article p')
    content2 = ''
    for i in content:
        if i.text[0:5] == '推薦閱讀：':
            pass
        elif i.text[0:5] == '延伸閱讀：':
            pass
        else:
            content2 += i.text
    return content2

def write_json(data_json):
    # 寫入json檔
    folder = newfolder(keyword)
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

def get_inside(keyword:str, pages:int):
    creatfolder(keyword)
    for page in range(1, pages+1):
        url = 'https://www.inside.com.tw/tag/{}?page={}'.format(keyword,page)
        soup = url_soup(url)
        allessay = soup.select('div[class="post_list post_list-list_style"]')
        # 頁面沒資料就結束
        if allessay == []:
            print('end',page,'page')
            break
        else:
            for essays in allessay:
                essay = essays.select('a.js-auto_break_title')
                for urls in essay:
                    url = urls['href']
                    get_data(url)
                    time.sleep(random.uniform(3, 10))
        # 第幾頁
        print(page,'page complete')

if __name__ == '__main__':
    keyword = input('keyword:')
    pages = int(input('page:'))
    get_inside(keyword,pages)
