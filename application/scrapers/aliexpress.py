import requests
import json
from application.scrapers.scraper import Scraper


class AliExpressScraper(Scraper):
    # Inherits from scraper.
    def extract_record(self):
        """ Extract the data of search_term from aliexpress.com."""
        records = {'product': []}
        url = "https://ali-express1.p.rapidapi.com/search"

        querystring = {"query": self.search_term, "page": "1"}

        headers = {
            'x-rapidapi-key': "9acf72976cmshbcd1f0f2fd610b9p16578ajsnadcd91620be1",
            'x-rapidapi-host': "ali-express1.p.rapidapi.com"
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