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
        # Configure basic chrome options 
        options = uc.ChromeOptions()
        # to turn off popups n shit
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        # This one saves all the profile info so it doesn't keep asking for the same shit lmao
        options.user_data_dir = "c:\\temp\\profile"
        # Trying to get rid of the password manager
        options.add_argument('--password_manager_enables=false')
        # Creates and returns the configured driver
        driver = uc.Chrome(options=options)
        return driver

    def tearDown(self):
        self.driver.quit()
        self.LOG('Finished doing my shit')
    
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
        self.LOG(f"Found {len(results)} results for the search")
        for i in results:
            self.LOG(i.text)
        return results

    def checkout_item(self, link:str, username:str, password:str, **kwargs):
        self.driver.get(link)
        # Finding the shipIt // Add to card button
        checkout_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.styles__ShippingWrapper-sc-13vnt8-0')
        ))
        # Get product name
        heading = self.driver.find_element_by_css_selector('.Heading__StyledHeading-sc-1mp23s9-0')
        heading_text = heading.find_element_by_tag_name('span').text
        # Check to make sure product name is the same as the link we went to
        if 'name' in kwargs.keys():
            name = kwargs['name']
            self.LOG(f"Looking for: {name}")
            assert name==heading_text, f'Link points to {heading_text} instead of {name}'
        # Add a check here if checkout_box.text matches r'Ship it' otherwise its out of stock
        buttons = self.driver.find_elements_by_tag_name('button')
        button = list(filter(lambda x: x.text=='Ship it', buttons))[0]
        button.click()
        # There's a popup here that I need to get past
            # This gives time for the popup to appear
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.styles__AddToCartHeading-mrt3qe-1')
        ))
        new_buttons = self.driver.find_elements_by_tag_name('button')
        checkout_button = list(filter(lambda x: x.text=='View cart & checkout', new_buttons))[0]
        checkout_button.click()
        # Move from cart to checkout section
        # Wait for new page to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.kmdQZX')
        ))
        more_buttons = self.driver.find_elements_by_tag_name('button')
        anotha_button = list(filter(lambda x: x.text=="I'm ready to check out", more_buttons))[0]
        anotha_button.click()
        # Allows target login to be skipped
        try:
            # Sign into target account
            username_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.NAME, 'username')
            ))
            password_input = self.driver.find_element_by_name('password')
            # Input username and password
            username_input.send_keys(username)
            password_input.send_keys(password)
            # Click the signin button
            so_many_buttons = self.driver.find_elements_by_tag_name('button')
            sign_in_button = list(filter(lambda x: x.text=="Sign in", so_many_buttons))[0]
            sign_in_button.click()
        except Exception as e:
            self.LOG('Skipped login page')
        # At this point target will either ask you to add a phone number, but if u alraedy
        # got one on ur account then it just lets you skip this part so...
        try:
            # check to see if it asks for a phone number, n if it does i skip it
            skip_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.hWNnTw')
            ))
            skip_btn.click()
        except Exception as e:
            self.LOG('No phone number page this time')
        # Finally fill out the personal information and the card shit
        try:
            # inna try block in case the personal informations already ready
            pass
        except Exception as e:
            self.LOG('Failed checkout process, please try again')

    # Logging functions easy to manipulate later
    def LOG(self, message:str) -> str:
        print(f"[{time.strftime('%H:%M:%S')}] " + message) # Temporary, will log to file eventually

    # Property functions for my sanity
    @property
    def current_url(self):
        return self.driver.current_url
