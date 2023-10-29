from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException


service = Service("C:/Windows/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://books.toscrape.com/")
print(driver.title)

records = []


def get_element_text_safe(css_selector):
    try:
        return driver.find_element(By.CSS_SELECTOR, css_selector).text
    except NoSuchElementException:
        return None


while True:  # Continúa hasta que no haya más páginas
    book_links = driver.find_elements(By.CSS_SELECTOR, "h3 a")
    book_links = [link.get_attribute("href") for link in book_links]

    for link in book_links:
        driver.get(link)
        title = get_element_text_safe("h1")
        price = get_element_text_safe(".price_color")
        stock = get_element_text_safe(".instock.availability")
        
        try:
            description = driver.find_element(By.CSS_SELECTOR, "#product_description + p").text
        except NoSuchElementException:
            description = None
            
        category = get_element_text_safe("ul.breadcrumb li:nth-child(3) a")

        book_data = {
            "title": title,
            "price": price,
            "stock": stock,
            "description": description,
            "category": category,
            "link": link
        }

        records.append(book_data)
        driver.back()  # Regresa a la página de lista de libros

    next_page = driver.find_elements(By.CSS_SELECTOR, "li.next a")
    if not next_page:
        break  # No hay más páginas, termina el loop
    next_page[0].click()  # Va a la siguiente página
    time.sleep(2)  # Espera antes de cargar la siguiente página para evitar sobrecargar el servidor

# Crear un DataFrame y guardar a CSV
df = pd.DataFrame(records)
df.to_csv("books.csv", index=False)

# Cerrar el navegador
driver.close()
