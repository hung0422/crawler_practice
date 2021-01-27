import os
import requests
import json
import pymysql
import dcard1
from dotenv import load_dotenv
load_dotenv()

# pymysql設定資料庫連線設定
host = os.getenv("host")
port = int(os.getenv("port"))
user = os.getenv("user")
passwd = os.getenv("passwd")
db = os.getenv("db")
charset = os.getenv("charset")

# 建立連線
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
# 建立游標
cursor = conn.cursor()

url = 'https://www.dcard.tw/service/api/v2/selections/forums/TW?sensitiveSelection=true'
# 爬蟲設定
ss = requests.session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

res = ss.get(url=url, headers=headers)
data = json.loads(res.text)

# 抓精選看板的文章
alllist = []
for i in data:
    alllist.append(dcard1.dcard_search(i['alias']))

# 將資料存到mysql
for sqllist in alllist:
    for sqltuple in sqllist:
        # 執行SQL語法
        sql = '''INSERT INTO dcard_test
            VALUES ('{}','{}','{}','{}');'''.format(*sqltuple)
        # 將指令放進cursor物件,並執行
        cursor.execute(sql)

# pymysql預設不會自動commit,所以要加這一行
conn.commit()

# 關閉游標及連線
cursor.close()
conn.close()