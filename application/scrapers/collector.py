from application.scrapers.scraper import Scraper
from application.scrapers.amazon import AmazonScraper
from application.scrapers.tapaz import TapazScraper
from application.scrapers.aliexpress import AliExpressScraper
from application.scrapers.data_handler import DataHandler

amazon: Scraper = AmazonScraper()
tapaz: Scraper = TapazScraper()
aliexpress: Scraper = AliExpressScraper()


class Collector:
    def __init__(self, choices, search_term, minimum, maximum, currency, sorting):
        self.choices = choices
        self.search_term = search_term
        self.minimum = minimum
        self.maximum = maximum
        self.currency = currency
        self.sorting = sorting
        self.all_records = {'amazon': {}, 'tapaz': {}, 'aliexpress': {}}

    def get_data(self):
        """ Implement all the options and get the results after handling(filtering and sorting) data."""
        for choice in self.choices:
            if choice == 'amazon':
                site = amazon
            elif choice == 'tapaz':
                site = tapaz
            elif choice == 'aliexpress':
                site = aliexpress
            site.set_search_term(self.search_term)
            records = site.extract_record()
            handler = DataHandler(records, self.minimum, self.maximum, self.currency, self.sorting)
            self.all_records[choice] = handler.handle_data()
        return self.all_records
