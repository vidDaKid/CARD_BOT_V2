# Testing functionality for the target app

from main import Target
import os, time

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

if __name__ == '__main__':
    start = time.time()
    target = Target()
    res = target.search_target('panini cards')
    target.checkout_item(
        res[0].get_attribute('href'),
        username,
        password,
        name=res[0].text, 
    )
    end = time.time()
    print(end - start)
    time.sleep(10)
    target.tearDown()
