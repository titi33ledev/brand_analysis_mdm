#%%
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
import concurrent.futures


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
    
# %%
def process(soup):
    titles = []
    prices = []
    brands = []
    url_products = []
    
    uri = "https://www.maisonsdumonde.com"
    
    titles_divs = soup.find_all('h2', class_='text-primary font-regular ds-body-m mb-2 h-[3em] line-clamp-2 after:absolute after:inset-0')
    prices_divs = soup.find_all('p', class_='text-primary-accent font-semibold ds-body-m inline-block')
    brands_divs = soup.find_all('p', attrs={'data-el': 'product-card__brand'})
    url_products_divs = soup.find_all('a', href=True)
    
    for url_product_div in url_products_divs:
        url = url_product_div['href']
        if url.startswith('/FR/fr/p/'):
            url_products.append(uri + url)
            
            
            title = url_product_div.find('h2', class_='text-primary font-regular ds-body-m mb-2 h-[3em] line-clamp-2 after:absolute after:inset-0')
            if title:
                title_text = title.get_text().strip()
            else:
                title_text = "NaN"
            titles.append(title_text)
            
            
            price = url_product_div.find_next('p', class_='text-primary-accent font-semibold ds-body-m inline-block')
            if price:
                price_text = price.get_text().strip().replace('\u202f', '').replace('€', '').replace(',', '.')
            else:
                price_text = "NaN"
            prices.append(price_text)
            
            
            brand_div = url_product_div.find_next('p', attrs={'data-el': 'product-card__brand'})
            if brand_div:
                brand_text = brand_div.get_text().strip()
            else:
                brand_text = "NaN"
            brands.append(brand_text)
            

    df = pd.DataFrame(
        {'titres': titles,
         'prix': prices,
         'marques': brands,
         'urls': url_products
         }
    )

    return df
# %%
def get_image_count(url):
    try:
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        time.sleep(random.randint(1, 5))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        media_gallery = soup.find('div', attrs={'data-el': 'media-gallery'})
        picture_tags = media_gallery.find_all('picture', {'data-el': 'ds-image'})
        image_count = len(picture_tags)
        
        driver.quit()
        
        
        return image_count
    
    
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération du nombre d'images pour l'URL {url}: {e}")
        return 0


#%%
def scrap_products_url(df, nom_colonne='urls'):
    nb_images = []
    descriptions = []

    if nom_colonne not in df.columns:
        print(f"La colonne '{nom_colonne}' n'existe pas dans le DataFrame.")
        return None

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        
        
        driver.get("https://www.maisonsdumonde.com/")
        time.sleep(random.randint(25, 30))
        
        
        button = driver.find_element(By.XPATH, '//*[@id="footer_tc_privacy_button_2"]')
        button.click()
        driver.quit()

        urls = df[nom_colonne].tolist()
        
        with tqdm.tqdm(total=len(urls), desc="Scraping URLs") as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(get_image_count, urls)
                for result in results:
                    nb_images.append(result)
                    pbar.update(1)

        df = pd.DataFrame({"nombres d'images": nb_images})
        return df
    
    
    except Exception as e:
        print(f"Une erreur s'est produite lors du scraping des URLs : {e}")
        return None

# %%
