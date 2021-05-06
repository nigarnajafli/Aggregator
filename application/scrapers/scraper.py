import abc
from application.scrapers.driver import Driver


class Scraper(metaclass=abc.ABCMeta):
	""" Initialize the values to be inherited in TapazScraper, AliExpressScraper, and AmazonScraper."""
	def __init__(self, timeout=0.4):
		self.search_term = None
		self.timeout = timeout
		# Initialize the driver object by using Driver class.
		self.driver_object = Driver()
		self.driver = self.driver_object.get_driver()

	def set_search_term(self, product):
		self.search_term = product

	@abc.abstractmethod
	def get_url(self):
		pass

	@abc.abstractmethod
	def get_source(self):
		pass

	@abc.abstractmethod
	def extract_record(self):
		pass