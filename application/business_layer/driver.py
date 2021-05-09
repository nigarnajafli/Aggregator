from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self):
        """ Initialize the Chrome Driver and make the scraping to run in the background."""
        self.chromeOptions = ChromeOptions()
        self.chromeOptions.add_argument("--window-size=1600, 490")
        self.chromeOptions.add_argument("--disable-infobars")
        self.chromeOptions.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chromeOptions)
        self.driver.implicitly_wait(30)

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.close()
        self.driver.quit()