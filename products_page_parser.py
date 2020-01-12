import re

import requests
from bs4 import BeautifulSoup

from database_connection import create_category, create_or_update_product

base_url = 'https://www.komputronik.pl/category'
menu_url = 'https://www.komputronik.pl/frontend-api/category/menu'

params = {
    'showBuyActiveOnly': 1,
    'sort': 1,
    'by': 'product_i18n_name',
    'showProducts': 1,
    'p': 1
}

price_pattern = re.compile(r'(\d+[,.]?\d*)')


def clean_name(name):
    return re.sub(r'\[.*\]', '', name).strip()


def clean_price(price):
    price_clean = price.replace('\xa0', '')
    search_result = price_pattern.search(price_clean)
    return float(search_result.group(1).replace(',', '.')) if search_result else None


def get_first_element(element_list):
    return element_list[0] if len(element_list) > 0 else None


def extract_item_data(item):
    name = get_first_element(item.select('a.blank-link'))
    price = get_first_element(item.select('span.price>span[class *= "price"]'))
    if name is None or price is None:
        return None
    return name.text.strip(), price.text.strip()


def parse_page(url, url_params, category_id):
    page = requests.get(url, url_params)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.select('ul li.product-entry2')
    result = [extract_item_data(x) for x in elements]
    clean_result = [{'name': clean_name(val[0]), 'price': clean_price(val[1])} for val in result if val is not None]
    for result in clean_result:
        create_or_update_product(result['name'], result['price'], category_id)


def get_category(category_url, category_id, category_name):
    request_url = base_url + category_url
    page = requests.get(request_url, params)
    create_category(category_id, category_name)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_count = int(soup.select('div.pagination > ul > li:nth-last-child(2)')[0].text)
    for i in range(page_count):
        params['p'] = i + 1
        print("retrieving category: {} page {} of {}".format(category_name, i + 1, page_count))
        parse_page(request_url, params, category_id)


if __name__ == "__main__":
    get_category('/1596/smartfony.html', 1596, 'smartfony')
    get_category('/5022/laptopy.html', 5022, 'laptopy')
    get_category('/8923/tablety.html', 8923, 'tablety')
