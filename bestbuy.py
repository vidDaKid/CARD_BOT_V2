# BestBuy Bot
# This is the proprty of V, don't steal this shit

import undetected_chromedriver.v2 as uc
import os, re, time, pickle

# selenium imports
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select 
# from selenium.webdriver.common.keys import Keys

# Honestly I should move move of the driver shit into a parent class that
# both bestbuy and target can pull off of so that I dont have to rewrite
# this shit / change it in 2 places but this bot gonna be deprecated soon
# so honestly fuck it
class BestBuy():
    def __init__(self):
        self.driver = self._driver_setup()

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
        driver.maximize_window()
        return driver

    # @param interval // Refreshes the page at every interval len (seconds)
    # @param timeout // Monitor mode ends after a certain timeout (seconds)
    def monitor_item(self, link:str, interval:int=5, timeout:int=300):
        # Get the link for the item ur monitoring
        self.driver.get(link)
        timeout_time = time.time() + timeout
        while True:
            self.driver.refresh()
            add_to_cart_btn = self.driver.find_element_by_css_selector('.add-to-cart-button')
            add_to_cart_btn = add_to_cart_btn.text
            if re.match(r'Add to Cart', add_to_cart_btn):
                self.LOG('item not availible')
            if re.match(r'Coming Soon', add_to_cart_btn):
                self.LOG('Item not yet released')
            if re.match(r'Out of Stock', add_to_cart_btn):
                self.LOG('Item out of stock')
            time.sleep(interval)
            if timeout_time < time.time():
                break


    def tearDown(self):
        self.driver.quit()
        self.LOG('Finished doing my shit')

    def LOG(self, message:str) -> str:
        print(str(time.strftime('%H:%M:%S')) + ' ' + message)
