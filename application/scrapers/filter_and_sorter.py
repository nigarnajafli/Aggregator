class CurrencyConverter:
    """The class for converting from one currency to another."""
    def __init__(self, convert_from, convert_to):
        self.convert_from = convert_from
        self.convert_to = convert_to
        self.currency_table = {'USD': {'USD': 1, 'AZN': 1.69898, 'RUB': 76.881848},
                              'AZN': {'USD': 0.58858982, 'AZN': 1, 'RUB': 45.251832},
                        'RUB': {'USD': 0.0130065, 'AZN': 0.0220986, 'RUB': 1}}

    def convert_currency(self):
        return self.currency_table[self.convert_from][self.convert_to]


class Filter:
    def __init__(self):
        self.options = {}

    def add_options(self, minimum, maximum, currency):
        self.options['minimum'] = minimum
        self.options['maximum'] = maximum
        self.options['currency'] = None if currency == 'default' else currency

    def filter_currency(self, records):
        """Find the currencies from currency table in CurrencyConverter class.
        Convert currencies."""
        currency = self.options['currency']
        if currency:
            for record in records['product']:
                currency_converter = CurrencyConverter(record['price_cur'], currency)
                record['price_val'] = round(record['price_val'] * currency_converter.convert_currency(), 2)
                record['price_cur'] = currency
        return records

    def filter_price(self, records):
        minimum = self.options['minimum']
        maximum = self.options['maximum']
        if minimum is None:
            records['product'] = list(filter(lambda elem: maximum >= elem['price_val'], records['product']))
        elif maximum is None:
            records['product'] = list(filter(lambda elem: minimum <= elem['price_val'], records['product']))
        else:
            records['product'] = list(filter(lambda elem: minimum <= elem['price_val'] <= maximum, records['product']))
        return records


class Sorter:
    """Sort the products in ascending or descending order of price."""
    def __init__(self):
        self.options = {}

    def add_options(self, sorting):
        self.options['sorting'] = None if sorting == 'default' else sorting

    def sort(self, records):
        sorting = self.options['sorting']
        if sorting == 'ascending':
            records['product'] = sorted(records['product'], key=lambda price: price['price_val'])
        elif sorting == 'descending':
            records['product'] = sorted(records['product'], key=lambda price: price['price_val'],
                                             reverse=True)
        return records