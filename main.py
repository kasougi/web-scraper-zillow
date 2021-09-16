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
    print('\r', f'Scrap url: {url}', end='')
    try:
        # Facts and Figures
        facts_and_figures = dr.driver.find_element_by_xpath('//*[@id="ds-container"]/div[4]/div[5]/div/nav/ul/li[2]/a')
        facts_and_figures.click()
        time.sleep(3)
        # See more facts and features
        see_more_facts = dr.driver.find_element_by_xpath('//*[@id="ds-data-view"]/ul/li[5]/div/div/div[3]/button/span')
        see_more_facts.click()
        time.sleep(3)
    except:
        dr.close()
        time.sleep(random.randint(1, 5))
        srap_home(url_data)
        return 1

    soup = BeautifulSoup(dr.driver.page_source, 'lxml')

    try:
        price = soup.find('div', {'class': 'ds-summary-row-container'}).findChild().findChild().findChild().text
        bd_ba_sqft = soup.find('div', {
            'class': 'ds-summary-row-container'}).findChild().findChild().findChild().next_sibling.text
        bd_ba_sqft = ''.join(i for i in bd_ba_sqft if i.isdigit() or i == ' ').split()
        adr = str(soup.find('h1', {'id': 'ds-chip-property-address'}).text).replace('\xa0', ' ')
        adr_city_zip = adr.split(', ')
    except:
        price = soup.find('div', {'class': 'Flex-c11n-8-48-0__sc-n94bjd-0 bqUhuP'}).findChild().text
        bd = soup.find('div', {'class': 'Flex-c11n-8-48-0__sc-n94bjd-0 bqUhuP'}).findChild().next_sibling.text
        ba = soup.find('div', {'class': 'Flex-c11n-8-48-0__sc-n94bjd-0 bqUhuP'}).findChild().next_sibling.next_sibling. \
            next_sibling.text
        sqft = soup.find('div',
                         {'class': 'Flex-c11n-8-48-0__sc-n94bjd-0 bqUhuP'}).findChild().next_sibling.next_sibling. \
            next_sibling.next_sibling.next_sibling.text
        bd_ba_sqft = [ba.split()[0], bd.split()[0], sqft.split()[0]]
        adr = str(soup.find('h1', {'class': 'qcc861-0 bUbZRQ sc-15x24q3-1 kySjPc'}).text).replace('\xa0', ' ')
        adr_city_zip = adr.split(', ')
        # print(adr_city_zip)
    overview = soup.find('div', {'class': "ds-overview-section"}).text.split('Read more')[0]
    overview = overview.replace('w/', '')
    dev = soup.find_all('div', {'class': 'sc-pjumZ gUhPC'})
    res = []
    for i in dev:
        res += i.text.split()
    str_j = ''.join(res)
    res_str = re.findall(r"[A-Z]?[^A-Z]*", str_j)
    dr.close()

    dict_for_save = get_dict_from_data(res_str, url, price, bd_ba_sqft, adr_city_zip, overview)
    save(dict_for_save, data_name)


def main(start_url):
    urls = set()
    for i in range(20):
        url = start_url + f'{i}_p'
        dr = ChromeDriverWithOptions(size=1)
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


if __name__ == '__main__':
    url = start.main()
    urls = list(main(url))
    if not urls:
        print('\r', "Nothing was found", end='')

    urls_new = []
    for u in urls:
        urls_new.append(u + '*:*' + url)

    p = Pool(processes=1)
    p.map(srap_home, urls_new)
