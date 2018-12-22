import sys
from save_urls import return_urls
from load import driver_chrome
from async_download import run_dowload

KEY_TITLES = ['Censo Escolar', 'Encceja', 'Prova Brasil', 'ANA', 'Enem', 'Enem por Escola']

def switch(option):
	if option == '--save_urls':
		driver, wait = driver_chrome('http://portal.inep.gov.br/microdados')
		return_urls(KEY_TITLES, driver)
		driver.close()
	if option == '--download':
		run_dowload()
	if option == '--check_zips':



