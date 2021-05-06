from application.scrapers.filter_and_sorter import Filter, Sorter

filter_ = Filter()
sorter = Sorter()


class DataHandler:
    # Has an Aggregation relationship with Filter and Sorter classes.
    def __init__(self, records, minimum, maximum, currency, sorting, filter_=filter_, sorter=sorter):
        self.records = records
        self.minimum = minimum
        self.maximum = maximum
        self.currency = currency
        self.sorting = sorting
        self.filter_ = filter_
        self.sorter = sorter

    def handle_data(self):
        """Get extracted records. Filter currencies, then select the products
        whose price is between minimum and maximum price values.
        Sort the filtered results in Ascending or Descending order."""
        self.filter_.add_options(self.minimum, self.maximum, self.currency)
        records = self.filter_.filter_currency(self.records)
        if self.minimum is not None or self.maximum is not None:
            records = self.filter_.filter_price(records)
        self.sorter.add_options(self.sorting)
        records = self.sorter.sort(records)
        return records