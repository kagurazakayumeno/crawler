import re
import os
import json
import requests
import threading
import datetime
from time import sleep
from random import random
from selenium import webdriver
from requests.cookies import RequestsCookieJar


def initialize(url):
    file = r"C:\Users\yumeno\AppData\Local\Google\Chrome\User Data"
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('blink-settings=imagesEnabled=false')
    option.add_argument('--no-sandbox')
    option.add_argument('--start-maximized')
    option.add_argument('user-data-dir=' + os.path.abspath(file))
    driver = webdriver.Chrome(options=option,
                              executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
    driver.get(url)
    return driver


def verify():
    url = 'https://www.pixiv.net/'
    driver = initialize(url)
    cookies = driver.get_cookies()
    with open("cookies.txt", "w") as f:
        json.dump(cookies, f)
    driver.close()
    jar = RequestsCookieJar()
    with open("cookies.txt", "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
    url = 'https://www.pixiv.net/bookmark_new_illust.php'
    html = requests.get(url, headers=headers, cookies=jar)
    if html.url != url:
        return None
    else:
        return jar


def download_img(img_url):
    img = s.get(img_url, headers=headers, cookies=jar)
    with open('pixiv/' + re.findall(r'/([0-9]*_.*?g)', img_url)[0], 'wb') as f:
        f.write(img.content)


def download_by_illust_id(illust_id):
    illust_url = f'https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=en'
    illust_html = s.get(illust_url, headers=headers, cookies=jar)
    if illust_html.json()['body']:
        img_urls = re.findall(r'https:\\/\\/i.pximg.net\\/img-original\\/img\\/.*?g', illust_html.text)
        for img_url in img_urls:
            img_url = re.sub(r'\\', '', img_url)
            download_img(img_url)
    else:
        print("The image doesn't exist")


def download_by_author_id(author_id):
    author_url = f'https://www.pixiv.net/ajax/user/{author_id}/profile/all?lang=en'
    author_html = s.get(author_url, headers=headers, cookies=jar)
    if author_html.json()['body']:
        illust_ids = author_html.json()['body']['illust'].keys()
        for illust_id in illust_ids:
            threading.Thread(target=download_by_illust_id, args=(illust_id,)).start()
            while threading.active_count() > 3:
                sleep(2 + random())
        print('Download complete')
    else:
        print("The author doesn't exist")


def download_by_following_list(page=5):
    if not os.path.exists('pixiv/following'):
        os.makedirs('pixiv/following')
    assert page > 0 and type(page) == int, 'The number entered should be positive integers.'
    url = 'https://www.pixiv.net/bookmark_new_illust.php'
    driver = initialize(url)
    sleep(random())
    for i in range(2, 1 + page):
        data = json.loads(driver.find_element_by_id('js-mount-point-latest-following').get_attribute('data-items'))
        illust_ids = [m['illustId'] for m in list(data)]
        for illust_id in illust_ids:
            threading.Thread(target=download_by_illust_id, args=(illust_id,)).start()
            while threading.active_count() > 3:
                sleep(2 + random())
        driver.find_element_by_xpath("//a[@rel='next']").click()
        print(f'Images on page {i} are downloaded complete')
    driver.close()


def download_by_ranking(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day, img_num=10):
    assert 0 < img_num <= 50 and type(img_num) == int, 'The number entered should be positive integers not more than 50.'
    assert year > 0 and month > 0 and day > 0 and type(year) == int and type(month) == int and type(day) == int, 'The date entered should be positive integers'
    lower_bound = datetime.datetime.strptime('2010-11-01', '%Y-%m-%d').date()
    date = datetime.datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
    if not os.path.exists(f'pixiv/ranking {date.strftime("%Y%m%d")}'):
        os.makedirs(f'pixiv/ranking {date.strftime("%Y%m%d")}')
    assert lower_bound <= date <= datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').date(), 'The date should be between 2010-11-01 and today.'
    url = f'https://www.pixiv.net/ranking.php?mode=daily&content=illust&date={date.strftime("%Y%m%d")}'
    driver = initialize(url)
    sleep(random())
    for i in range(1, 1 + img_num):
        illust_id = driver.find_element_by_xpath(f"//section[@id='{i}']").get_attribute('data-id')
        threading.Thread(target=download_by_illust_id, args=(illust_id,)).start()
        while threading.active_count() > 3:
            sleep(2 + random())
    print('Download successfully')
    driver.close()


if __name__ == '__main__':
    if not os.path.exists('pixiv'):
        os.makedirs('pixiv')
    os.system('taskkill /f /im %s' % 'chrome.exe')
    headers = {'referer': 'https://www.pixiv.net',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    jar = verify()
    if jar:
        s = requests.Session()
        s.keep_alive = False
        # do something
        s.close()
    else:
        print('Please check login information.')
