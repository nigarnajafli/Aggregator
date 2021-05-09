from bs4 import BeautifulSoup
import time
from .scraper import Scraper


class AmazonScraper(Scraper):
    # Inherits from Scraper
    def get_url(self):
        """Generate a url from search term"""
        template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
        self.search_term = self.search_term.replace(' ', '+')

        # add term query to url
        url = template.format(self.search_term)

        # add page query placeholder
        url += '&page={}'
        return url

    def get_source(self):
        pass

    @staticmethod
    def get_page_count(soup):
        """Amazon has pagination and splits the contents of the website into discrete pages.
        Find the number of pages in result."""
        page_count = 1
        try:
            pages = soup.find_all("ul", class_="a-pagination")
            for page in pages:
                page_number = page.text.strip()
            numbers = list(str(page_number).split('\n'))
            for number in numbers:
                try:
                    if int(number) > page_count:
                        page_count = int(number)
                except:
                    continue
        except:
            pass

        return page_count

    def extract_record(self):
        """Extract and return data from a single record"""
        records = {'product': []}
        url_page = self.get_url()
        self.driver.get(url_page.format(1))
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        page_count = self.get_page_count(soup)
        # Loop over all the pages.
        for page in range(1, page_count):
            self.driver.get(url_page.format(page))
            time.sleep(self.timeout)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            results = soup.find_all('div', {'data-component-type': 's-search-result'})
            for item in results:
                atag = item.h2.a
                description = atag.text.strip()
                url = 'https://www.amazon.com' + atag.get('href')
                try:
                    # Price can contain currency sign, space and comma.
                    # Extract the price value from price section
                    price_parent = item.find('span', 'a-price')
                    price = price_parent.find('span', 'a-offscreen').text
                    if '$' in price:
                        price = price.replace('$', '')
                    if ' ' in price:
                        price = str(price).replace(' ', '')
                    if ',' in price:
                        price = price.replace(',', '')
                    price_val = float(price)
                    price_cur = 'USD'
                except AttributeError:
                    continue

                try:
                    # rank and rating
                    rating = item.i.text
                    review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
                except AttributeError:
                    rating = ''
                    review_count = ''

                record = (description, price_val, price_cur, rating, review_count, url)
                if record:
                    records['product'].append({
                        'description': description,
                        'price_val': price_val,
                        'price_cur': price_cur,
                        'rating': rating,
                        'review_count': review_count,
                        'url': url
                    })
        return records
