from load_selenium import driver_chrome


def return_urls(titles):
	driver, wait = driver_chrome('http://portal.inep.gov.br/microdados')

	# Return selenium elements with name that is singular on the page
	# If the name is not singular raise errors
	def single_elements_parents(elem_name: str, text_list :list, driver):
		interest_elements = []
		for text_str in text_list:

			found = driver.find_elements_by_xpath('//%s[(text()=\'%s\')]/parent::div'%(elem_name, text_str))
			if len(found) == 0:
				raise Exception('%s Not found' % text_str)
			elif len(found) == 1:
				interest_elements.append(tuple((text_str, found[0])))
			else:
				raise Exception('Two elements with the same name %s' % text_str)
		return interest_elements

	# Return the dicts with the names of the projects, year of the info and url
	def get_zip_by_years(list_elements):
		zip_list = []
		for elem_obj in list_elements:
			urls = elem_obj[1].find_elements_by_xpath(".//a[contains(@href,'.zip')]")
			if len(urls) > 0:
				for url in urls:
					zip_list.append(
						{'title': elem_obj[0], 'zip_url': url.get_attribute('href'), 'year': url.get_attribute('text')})
			else:
				raise print()
		return zip_list

	programs = single_elements_parents(elem_name='h4', text_list=titles, driver=driver)
	programs = get_zip_by_years(programs)
	driver.close()
	return programs