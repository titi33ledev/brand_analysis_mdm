#%%
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#%%
def scrap(mot_cles):
    
    driver = webdriver.Chrome()
    driver.get("https://www.maisonsdumonde.com/")

    time.sleep(random.randint(25, 30))

    button = driver.find_element(By.XPATH, '//*[@id="footer_tc_privacy_button_2"]')
    button.click()

    time.sleep(random.randint(4,8))

    search_bar = driver.find_element(By.XPATH, '//*[@id="search-bar"]/input')
    search_bar.send_keys(mot_cles)
    search_bar.send_keys(Keys.RETURN)

    time.sleep(random.randint(5, 10))

    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')
# %%
