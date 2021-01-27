import os
import time
import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
load_dotenv()

# 現在時間
locTime = datetime.datetime.now()
# 運算日期為-1天
delta=datetime.timedelta(days=-1)
# 昨天日期
yesterday = locTime+delta
strtime =yesterday.strftime('%Y%m%d')

# 帳號&密碼
gmail_account = os.getenv("gmail_account")
gmail_password = os.getenv("gmail_password")

driver = Chrome('chromedriver')
# google首頁
url = 'https://www.google.com.tw/'
driver.get(url)

# 進入gmail登入頁面
driver.find_element_by_link_text('Gmail').click()
driver.find_element_by_link_text('Sign in').click()

# 所有網頁視窗的控制代碼
windows = driver.window_handles
# 進入最新開啟的視窗
driver.switch_to.window(windows[-1])
# 輸入帳號
driver.find_element_by_id('identifierId').send_keys(gmail_account)
driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
# 等待網頁
time.sleep(2)
# 輸入密碼
driver.find_element_by_name('password').send_keys(gmail_password)
driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
time.sleep(5)

# 尋找所有信件標題
alltitle = driver.find_elements_by_class_name('y6')
for i in alltitle:
    # 尋找符合條件的信件
    if strtime in i.text:
        i.click()
        # 定位到要懸停的位置
        element = driver.find_element_by_class_name('aYv')
        # 對定位到的位置執行滑鼠懸停操作
        ActionChains(driver).move_to_element(element).perform()
        # 下載檔案
        driver.find_element_by_class_name('wkMEBb').click()
        time.sleep(3)
        break

# 關閉視窗
driver.quit()

