#%%
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

#%%
def scrap_first_page(mot_cles):
    
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
    driver.implicitly_wait(20)
    
    scrolling_bar = driver.find_element(By.XPATH,'/html/body/div[1]/main/section/div/div/section/div[3]/div[3]/div/div/div/button')
    
    while True: 
        
        try:
            
            scrolling_bar.click()
            driver.implicitly_wait(3)
            
        except:
            
            break
                
    page_source = driver.page_source
    
    return BeautifulSoup(page_source, 'html.parser')


#%%

def scrap_data_products(soup):
    
    
# %%
def process(soup):
    
    titles = []
    prices = []
    product_urls = []
    
    titles_divs = soup.find_all('h2', class_='text-primary font-regular ds-body-m mb-2 h-[3em] line-clamp-2 after:absolute after:inset-0')
    prices_divs = soup.find_all('p', class_='text-primary-accent font-semibold ds-body-m inline-block')
    brand_divs = soup.find_all('p', attrs={'data-el': 'product-card__brand'})

    
    brand_divs = soup.find_all('p', attrs={'data-el': 'product-card__brand'})
    
    for brand_div in brand_divs:
        link_div = brand_div.find_next('a', attrs={'data-el': 'resolver-link'})
        if link_div is not None:
            product_url = link_div['href']
            product_urls.append(product_url)
    
    
    
    for titles_div, prices_div, product_url in zip(titles_divs, prices_divs, product_urls):
        price = prices_div.get_text().strip().replace('\u202f', '').replace('€', '').replace(',', '.') if prices_div else "NaN"
        title = titles_div.get_text().strip()

        titles.append(title)
        prices.append(price)


    df = pd.DataFrame(
        {'titres' : titles,
        'prix' : prices,
        'url_produits' : product_url
        }
    )
    
    return df
# %%
def scrap_product_url(df,nom_colonne='url_produits'):
    
    nb_images = []
    descriptions = []
    uri = "https://www.maisonsdumonde.com/"
    
    if nom_colonne not in df.columns:
        print(f"La colonne '{nom_colonne}' n'existe pas dans le DataFrame.")
        return None
    
    for index, row in df.iterrows():
        driver = webdriver.Chrome()
        lien = uri + row['url_produits']    
        driver.get(lien)
        
        time.sleep(random.randint(10,20))
        
        button = driver.find_element(By.XPATH, '//*[@id="footer_tc_privacy_button_2"]')
        button.click()
        
        page_source = driver.page_source
        
        driver.implicitly_wait(7)
        
        pagination_buttons = soup.find_all('button', attrs={'data-el': 'ds-pager__bullet'})
        nombre_images = len(pagination_buttons)        
        product_description = soup.find('div', attrs={'data-v-cd98ad86': '', 'data-el': 'product-description-panel__rich-text'})

        nb_images.append(nombre_images)
        descriptions.append(product_description)
        
        
    df = pd.DataFrame(
    {"nombres d'images" : nb_images,
        "descriptions" : descriptions
        }
    )
    
    return df
        
        
# %%
