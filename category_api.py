import requests
import json

komputronik_category_api = "https://www.komputronik.pl/frontend-api/category/menu"


class Category:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url


def get_category_map():
    response = requests.get(komputronik_category_api)
    parsed_response = json.loads(response.content)
    category_dictionary = dict()
    for category_list in parsed_response.values():
        for item in category_list:
            category_dictionary[item['name']] = Category(item["id"], item['name'], item['url'])
    return category_dictionary
