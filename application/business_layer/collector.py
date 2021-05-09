from .scraper import Scraper
from .amazon import AmazonScraper
from .tapaz import TapazScraper
from .aliexpress import AliExpressScraper
from .data_handler import DataHandler

amazon: Scraper = AmazonScraper()
tapaz: Scraper = TapazScraper()
aliexpress: Scraper = AliExpressScraper()
handler = DataHandler()


class Collector:
    def __init__(self, choices, search_term, minimum, maximum, currency, sorting):
        self.choices = choices
        self.search_term = search_term
        self.minimum = minimum
        self.maximum = maximum
        self.currency = currency
        self.sorting = sorting
        self.all_records = {'amazon': {}, 'tapaz': {}, 'aliexpress': {}}
        self.amazon = amazon
        self.tapaz = tapaz
        self.aliexpress = aliexpress
        self.handler = handler


    def get_data(self):
        """ Implement all the options and get the results after handling(filtering and sorting) data."""
        for choice in self.choices:
            if choice == 'amazon':
                site = self.amazon
            elif choice == 'tapaz':
                site = self.tapaz
            elif choice == 'aliexpress':
                site = self.aliexpress
            site.set_search_term(self.search_term)
            records = site.extract_record()
            self.all_records[choice] = self.handler.handle_data(records, self.currency, self.minimum, self.maximum, self.sorting)
        return self.all_records
