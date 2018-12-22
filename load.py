from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


def driver_chrome(url):

	options = Options()
	options.add_argument('--headless')
	driver = webdriver.Chrome(chrome_options=options)
	wait = WebDriverWait(driver, 20)
	driver.get(url)

	return driver, wait
