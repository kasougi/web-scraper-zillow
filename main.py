import json
from bs4 import BeautifulSoup
import time
from Driverconnect import ChromeDriverWithOptions
from data_refactor import get_dict_from_data
import csv
from selenium.webdriver import ActionChains
import random
import os
from multiprocessing import Pool
from start_url import add_to_url


def check_capch(dr):
    try:
        element = dr.driver.find_element_by_id('px-captcha')
        action = ActionChains(dr.driver)
        action.click_and_hold(element)
        action.perform()
        time.sleep(11)
        action.release(element)
        action.perform()
        time.sleep(0.2)
        action.release(element)
        time.sleep(5)
    except:
        return


def save(dict, name):
    name = name.split('www.zillow.com/')[1]
    name = name.replace('/', '_')

    def new():
        os.chdir(path='.')
        with open(f"./data/{name}.csv", "w+") as f:
            w = csv.DictWriter(f, dict.keys())
            w.writeheader()
            w.writerow(dict)

    try:
        os.mkdir('data')
        new()
    except:
        ls = os.listdir(path="./data")
        if f'{name}.csv' in ls:
            try:
                os.chdir(path='.')
                with open(f"./data/{name}.csv", "a") as f:
                    w = csv.DictWriter(f, dict.keys())
                    w.writerow(dict)
            except Exception as ex:
                time.sleep(5)
                save(dict, name)
                return
        else:
            new()


def srap_home(url_data):
    url = url_data.split('*:*')[0]
    zpid = url.split('/')[-2].replace('_zpid', '')
    data_name = url_data.split('*:*')[1]
    dr = ChromeDriverWithOptions()
    dr.get_from_url(url)
    time.sleep(5)
    check_capch(dr)
    print(f'\nScrap url: {url}')
    time.sleep(3)
    soup = BeautifulSoup(dr.driver.page_source, 'lxml')
    json_from_html = soup.find('script', {'id': 'hdpApolloPreloadedData'})
    dr.close()
    txt = list(json_from_html.text)
    for i in range(len(txt)):
        if txt[i] == "\\":
            if txt[i + 1] != "\\":
                pass
            elif txt[i + 1] == "\\" and txt[i + 2] == "\\":
                txt[i + 3] = "'"
    len_for_json = len(zpid) + 10
    dfj = json.loads(''.join(txt).replace('\\', '')[13:-len_for_json])
    dict_for_save = get_dict_from_data(dfj, zpid)
    save(dict_for_save, data_name)


def get_links(start_url):
    urls = set()
    sort = ["globalrelevanceex_sort",
            "priced_sort",
            "pricea_sort",
            "days_sort",
            "beds_sort",
            "baths_sort",
            "size_sort",
            "lot_sort",
            ]
    need_sort = 1
    for srt in sort:
        if need_sort:
            for i in range(21):
                url = start_url + f'{srt}/{i}_p/'
                dr = ChromeDriverWithOptions()
                try:
                    dr.get_from_url(url)
                except:
                    dr.close()
                    return urls
                time.sleep(5)
                ir = 0
                check_capch(dr)
                while ir + 200 <= 1080 * 14:
                    krtk = '/' if random.randint(1, 2) % 2 else '\\'
                    print('\r', f'{krtk} We get links: page {i}', end='')
                    # Scroll down to bottom
                    dr.driver.execute_script(f"window.scrollTo({ir}, {ir + 200});")
                    ir += 200
                    # Wait to load page
                    time.sleep(0.18)
                time.sleep(3)
                # Получаем ссылку
                soup = BeautifulSoup(dr.driver.page_source, 'lxml')
                try:
                    total_count = int(soup.find('div', {'class': 'total-text'}).text.replace(',', ''))
                    if total_count <= 500 and i == 0:
                        need_sort = 0
                except:
                    pass
                cards = soup.find_all('a', {'class': 'list-card-link'})
                urls.update(set(i['href'] for i in cards))
                time.sleep(1)
                dr.close()
    else:
        return urls


def main():
    url = add_to_url()
    print(url)
    urls = list(get_links(url))
    if not urls:
        print('\r', "Nothing was found", end='')
        return
    urls_new = []
    for u in urls:
        urls_new.append(u + '*:*' + url)
    p = Pool(processes=8)
    p.map(srap_home, urls_new)


if __name__ == '__main__':
    main()