import math
from os.path import exists

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import requests
import re

# Make folder to save images
FOLDER_NAME = "downloaded_images"
os.makedirs(FOLDER_NAME, exist_ok=True)

# Initialize driver
driver = webdriver.Chrome()
driver.get("https://www.daraz.com.bd/mens-shoes/")
driver.refresh()
driver.maximize_window()
time.sleep(2)

# Store all image links
image_links = []


# Find all products in a text
try:
    total_product_text = driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div/div/span[1]').text
    total_product = int(re.search(r'\d+', total_product_text).group())

    # Total product in a single page
    products = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div')
    total_product_per_page = len(products)

    # Total page calculate
    total_page = math.ceil(total_product / total_product_per_page)


    for page in range(1, total_page):
        # get page url using pagination
        driver.get(f"https://www.daraz.com.bd/mens-shoes/?page={page}")

        try:
            product_section = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]')
            product_section_height = driver.execute_script('return arguments[0].scrollHeight;', product_section)
            time.sleep(2)

            for i in range(0, product_section_height, 50):
                driver.execute_script(f'window.scrollTo(0, {i})')
                time.sleep(1)
        except Exception as e:
            print(e)

        for i in range(1, total_product_per_page):
            link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{i}]/div/div/div[1]/div/a/div/img').get_attribute("src")
            image_links.append(link)


    time.sleep(5)
    driver.quit() # close the browser

except Exception as e:
    print(e)

# download all image
for i, image_url in enumerate(image_links):
    response = requests.get(image_url, stream=True)
    with open(os.path.join(FOLDER_NAME, f"shoes_{i+1}.png"), 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

print("Image Download Successfully")

