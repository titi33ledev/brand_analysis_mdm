#%%
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

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

    time.sleep(random.randint(10, 35))

    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')
# %%
def process(soup):
    
    number_of_products = []
    titles = []
    prices = []
    
    nb_products_divs = soup.find_all({"class" : "text-primary font-regular ds-body-m"})
    titles_divs = soup.find_all({"class" : "text-primary font-regular ds-body-m mb-2 h-[3em] line-clamp-2 after:absolute after:inset-0"})
    prices_divs = soup.find_all({"class" : "text-primary-accent font-semibold ds-body-m inline-block"})
    
    for nb_products_div, titles_div, prices_div in zip(nb_products_divs,titles_divs,prices_divs):
        
        nb_products = nb_products_div.get_text().strip()
        price = prices_div.get_text().strip().replace('\u202f', '').replace('€', '').replace(',', '.') if prices_div else "NaN"
        title = titles_div.get_text().strip()
        
        titles.append(title)
        prices.append(price)
        number_of_products.append(nb_products)


    df = pd.DataFrame(
        {'titres' : titles,
        'prix' : prices,
        'nombres_de_produits': number_of_products,
        }
    )
    
    return df
# %%
