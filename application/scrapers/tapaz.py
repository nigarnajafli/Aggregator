import time
from bs4 import BeautifulSoup
from application.scrapers.scraper import Scraper


class TapazScraper(Scraper):
	# Inherits from Scraper.
	def get_url(self):
		"""Generate a url from search term"""
		template = 'https://tap.az/elanlar?keywords={}'
		self.search_term = self.search_term.replace(' ', '+')

		# add term query to url
		url = template.format(self.search_term)
		return url

	def get_source(self):
		""" As Tapaz does not upload the whole page at once and
		the content is loaded when the user scrolls down,
		Get the whole source page of Tapaz."""
		self.driver.get(self.get_url())
		scrolls = 0
		end_of_page = False
		last = self.driver.execute_script("return document.body.scrollHeight")
		while not end_of_page:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(self.timeout)
			new = self.driver.execute_script("return document.body.scrollHeight")
			if last == new:
				end_of_page = True
			else:
				last = new
			scrolls += 1
		return self.driver.page_source

	def extract_record(self):
		""" Extract the records corresponding to search term."""
		records = {'product': []}
		whole = self.get_source()
		start = '<div class="js-endless-container products endless-products">'
		end = '<div class="pagination_loading">'
		product_info = str(whole)[str(whole).find(start):str(whole).find(end)]
		soup = BeautifulSoup(product_info, 'lxml')

		# The part where the information about matching products is located
		results = soup.select("div[class^=products-i]")
		for item in results:
			for link in item.find_all('a', class_='products-link', href=True):
				try:
					# The name part of the product
					description = link.find('div', class_='products-name').text.strip()
					url = 'https://tap.az' + link['href']
					price = link.find('span', class_='price-val').text
					# Price parts can contain currency, space, or comma.
					# Extract the price value from this price part.
					if '$' in price:
						price = price.replace('$', '')
					if ' ' in price:
						price = str(price).replace(' ', '')
					if ',' in price:
						price = price.replace(',', '.')
					price_val = float(price)
					price_cur = link.find('span', class_='price-cur').text
				except:
					continue

				records['product'].append({
					'description': description,
					'price_val': price_val,
					'price_cur': price_cur,
					'rating': None,
					'review_count': None,
					'url': url
				})
		return records