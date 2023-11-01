from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
import re  # Para procesar las cadenas y extraer el número de la disponibilidad

service = Service("C:/Windows/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://books.toscrape.com/")
print(driver.title)

records = []
book_id = 1  # Inicializar el ID del libro

def get_element_text_safe(css_selector):
    try:
        return driver.find_element(By.CSS_SELECTOR, css_selector).text
    except NoSuchElementException:
        return None

def get_element_text_after_th(th_text):
    rows = driver.find_elements(By.CSS_SELECTOR, "table th")
    for row in rows:
        if row.text == th_text:
            return row.find_element(By.XPATH, "following-sibling::td").text
    return None

def get_star_rating():
    try:
        star_element = driver.find_element(By.CSS_SELECTOR, "p.star-rating")
        return star_element.get_attribute("class").split(" ")[1]
    except NoSuchElementException:
        return None



while True:
    book_links = driver.find_elements(By.CSS_SELECTOR, "h3 a")
    book_links = [link.get_attribute("href") for link in book_links]

    for link in book_links:
        driver.get(link)
        title = get_element_text_safe("h1")
        price = get_element_text_safe(".price_color")
        stock_text = get_element_text_safe(".instock.availability")
        stock_number = int(re.search(r'(\d+)', stock_text).group()) if stock_text else None

        try:
            description = driver.find_element(By.CSS_SELECTOR, "#product_description + p").text
        except NoSuchElementException:
            description = None

        category = get_element_text_safe("ul.breadcrumb li:nth-child(3) a")
        image_url = driver.find_element(By.CSS_SELECTOR, ".carousel-inner img").get_attribute("src")
        star_rating = get_star_rating()

        upc = get_element_text_after_th('UPC')
        product_type = get_element_text_after_th('Product Type')
        price_excl_tax = get_element_text_after_th('Price (excl. tax)')
        price_incl_tax = get_element_text_after_th('Price (incl. tax)')
        tax = get_element_text_after_th('Tax')
        reviews = get_element_text_after_th('Number of reviews')

        book_data = {
            "ID": book_id,
            "title": title,
            "price": price,
            "stock": stock_number,
            "description": description,
            "category": category,
            "link": link,
            "image_url": image_url,
            "star_rating": star_rating,
            "upc": upc,
            "product_type": product_type,
            "price_excl_tax": price_excl_tax,
            "price_incl_tax": price_incl_tax,
            "tax": tax,
            "number_of_reviews": reviews
        }

        records.append(book_data)
        book_id += 1
        driver.back()

    next_page = driver.find_elements(By.CSS_SELECTOR, "li.next a")
    if not next_page:
        break
    next_page[0].click()
    time.sleep(2)

df = pd.DataFrame(records)
df.to_csv("books4.csv", sep=";", index=False)

driver.close()
