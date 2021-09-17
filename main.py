from bs4 import BeautifulSoup
import time
from Driverconnect import ChromeDriverWithOptions
from data_refactor import get_dict_from_data
import re
import csv
from selenium.webdriver import ActionChains
import random
import os
from multiprocessing import Pool
import start
import pprint


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
    data_name = url_data.split('*:*')[1]
    dr = ChromeDriverWithOptions()
    dr.get_from_url(url)
    time.sleep(5)
    check_capch(dr)
    print(f'\nScrap url: {url}')
    time.sleep(5)
    dr.driver.execute_script(f"window.scrollTo(100, 300);")
    try:
        # Facts and Figures
        facts_and_figures = dr.driver.find_element_by_xpath('//*[@id="ds-data-view"]/div[2]/div/nav/ul/li[2]/a')
        facts_and_figures.click()
        time.sleep(5)
        # See more facts and features
        see_more_facts = dr.driver.find_element_by_xpath('//*[@id="ds-data-view"]/ul/li[5]/div/div/div[3]/button/span')
        see_more_facts.click()
        time.sleep(5)
    except Exception as ex:
        print(ex)
        dr.close()
        time.sleep(random.randint(1, 5))
        srap_home(url_data)
        return 1
    soup = BeautifulSoup(dr.driver.page_source, 'lxml')
    dr.close()
    price = soup.find('div', {"id": "ds-data-view"}).findChild().findChild().findChild().findChild().text
    bd = soup.find('div', {"id": "ds-data-view"}).findChild().findChild().findChild().findChild().next_sibling.text
    ba = soup.find('div', {"id": "ds-data-view"}).findChild().findChild().findChild().findChild().next_sibling.next_sibling.next_sibling.text
    sqft = soup.find('div', {"id": "ds-data-view"}).findChild().findChild().findChild().findChild().next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
    bd_ba_sqft = [ba.split()[0], bd.split()[0], sqft.split()[0] + sqft.split()[1]]
    adr = soup.find('div', {'id': 'ds-data-view'}).findChild().find('h1').text.replace('\xa0', ' ')
    adr_city_zip = adr.split(', ')
    overview = soup.find('div', {'class': "ds-overview-section"}).text.split('Read more')[0]
    overview = overview.replace('w/', '')
    dev = soup.find('div', {"id": "ds-data-view"}).findChild().next_sibling.next_sibling.findChild().next_sibling.next_sibling.next_sibling.next_sibling.findChild().next_sibling.findChild()
    dev = dev.text.split('Interior details')[1]
    dev = ''.join(dev.split())
    res_str = re.findall(r"[A-Z]?[^A-Z]*", dev)
    dict_for_save = get_dict_from_data(res_str, url, price, bd_ba_sqft, adr_city_zip, overview)
    pprint.pprint(dict_for_save)
    save(dict_for_save, data_name)


def get_links(start_url):
    urls = set()
    for i in range(1):
        url = start_url + f'{i}_p'
        dr = ChromeDriverWithOptions()
        dr.get_from_url(url)
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
        cards = soup.find_all('a', {'class': 'list-card-link'})
        urls.update(set(i['href'] for i in cards))
        time.sleep(1)
        dr.close()
    else:
        return urls


def main():
    url = start.main()
    urls = list(get_links(url))
    if not urls:
        print('\r', "Nothing was found", end='')
        return
    urls_new = []
    for u in urls:
        urls_new.append(u + '*:*' + url)
    # srap_home()
    p = Pool(processes=8)
    p.map(srap_home, urls_new)


if __name__ == '__main__':
    main()
