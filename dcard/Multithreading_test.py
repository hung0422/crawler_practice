import concurrent.futures
import dcard1
import time


def threading(test):
    dcard1.dcard_search(test)

if __name__ == '__main__':
    start_time = time.time()
    testlist = ['funny','mood']
    # 同時建立及啟用執行緒
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(threading, testlist)
    # for i in testlist:
    #     threading(i)
    end_time = time.time()
    print('幾秒:', end_time-start_time)

