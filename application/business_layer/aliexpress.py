import requests
import json
from .scraper import Scraper
from .json_parser import Parser
parser = Parser('values.json')


class AliExpressScraper(Scraper):
    # Inherits from scraper.
    def extract_record(self):
        """ Extract the data of search_term from aliexpress.com."""
        records = {'product': []}
        url = parser.get_value("url_for_aliexpress")

        querystring = {"query": self.search_term, "page": "1"}

        headers = {
            'x-rapidapi-key': parser.get_value("x-rapidapi-key"),
            'x-rapidapi-host': parser.get_value("x-rapidapi-host")
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        dictdump = json.loads(str(response.text))
        item_list = dictdump['data']['searchResult']['mods']['itemList']['content']
        base_url = 'https://www.aliexpress.com/item/'

        for item in item_list:
            # Grabs the product name, price value, currency,
            # product ID, and rating from the results.
            description = item['title']['displayTitle']
            price_val = item['prices']['sale_price']['minPrice']
            price_cur = item['prices']['sale_price']['currencyCode']
            product_id = item['productId']
            try:
                rating = item['evaluation']['starRating']
            except:
                rating = None

            records['product'].append({
                'description': description,
                'price_val': price_val,
                'price_cur': price_cur,
                'rating': rating,
                'review_count': None,
                'url': base_url + str(product_id) + '.html'
            })
        return records

    def get_url(self):
        pass

    def get_source(self):
        pass