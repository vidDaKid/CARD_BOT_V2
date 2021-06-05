 # CARD_BOT_V2 // Heavy focus on avoiding bot detection 
# This is the sole property of V, if you steal it i'll fuck you up (prolly not but still dont)

import undetected_chromedriver.v2 as uc
import os, re, time

# selenium imports
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select 
# from selenium.webdriver.common.keys import Keys

class Target:
    def __init__(self):
        self.driver = self._driver_setup()
        self.LOG('Starting up new driver instance')

    def _driver_setup(self):
        # Currently just creates and sends it out
        driver = uc.Chrome()
        return driver
    
    # This functions searches target & returns a list of webdrivers as output
    # but it wont let me typecast that so its just list lmao
    def search_target(self, search_query:str) -> list:
        self.LOG(f'Starting search for: {search_query}')
        search_link = f"https://www.target.com/s?searchTerm={search_query.replace(' ', '+')}"
        self.driver.get(search_link)
        # Filter results to get only relevant info
        res = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.jBYETz')
        ))
        # Filters for all of the non-empty links in the <ul>
        results = [x for x in res.find_elements_by_tag_name('a') if x.text!='']
        # Filters to remove any rating elements
        results = [x for x in results if not re.match(r'.* out of 5', x.text)]
        # Filter out all of the manufacture names
        results = list(filter(lambda x: x.value_of_css_property('font-size')=='16px', results))
        return results

    # Logging functions easy to manipulate later
    def LOG(self, message:str) -> str:
        print(f"[{time.strftime('%H:%M:%S')}] " + message) # Temporary, will log to file eventually

    # Property functions for my sanity
    @property
    def current_url(self):
        return self.driver.current_url
