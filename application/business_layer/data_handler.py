from .filter_and_sorter import Filter, Sorter

filter_ = Filter()
sorter = Sorter()


class DataHandler:
    # Has an Aggregation relationship with Filter and Sorter classes.
    def __init__(self):
        self.filter_ = filter_
        self.sorter = sorter

    def handle_data(self, records, currency, minimum, maximum, sorting):
        """Get extracted records. Filter currencies, then select the products
        whose price is between minimum and maximum price values.
        Sort the filtered results in Ascending or Descending order."""
        records = self.filter_.filter_currency(records, currency)
        if minimum is not None or maximum is not None:
            records = self.filter_.filter_price(records, minimum, maximum)
        records = self.sorter.sort(records, sorting)
        return records