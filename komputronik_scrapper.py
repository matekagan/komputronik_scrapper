import sys

from category_api import get_category_map
from products_page_parser import get_category

categories = get_category_map()


def print_options():
    print("---- Komputronik Price Scrapper ----")
    print("parameters:")
    print("show                                 --- prints all possible categories to retrieve")
    print("check_category [category_name] ...   --- gathers data for selected categories")
    print("parseall                             --- gathers data for all available categories")


def main(args):
    if len(args) == 0:
        print_options()
    else:
        handle_arguments(args)


def show():
    for category_name in categories.keys():
        print(category_name)


def get_categories(params):
    for category_name in params:
        category = categories[category_name.strip()]
        if category:
            get_category(category)


def get_all_categories():
    for category in categories.values():
        get_category(category)


def handle_arguments(arguments):
    command = arguments[0].strip()
    if command == "show":
        show()
    elif command == "parseall":
        get_all_categories()
    elif command == "check_category" and len(arguments) > 1:
        get_categories(arguments[1:])


if __name__ == "__main__":
    main(sys.argv[1:])
