from os.path import exists

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import requests

# Make folder to save images
FOLDER_NAME = "downloaded_images"
os.makedirs(FOLDER_NAME, exist_ok=True)

# Initialize driver
driver = webdriver.Chrome()
driver.get("https://www.daraz.com.bd/mens-shoes/")
driver.refresh()
driver.maximize_window()
time.sleep(2)

image_links = []

for i in range(1, 41):
    link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{i}]/div/div/div[1]/div/a/div/img').get_attribute("src")
    image_links.append(link)


time.sleep(5)
driver.quit() # close the browser

# download all image
for i, image_url in enumerate(image_links):
    response = requests.get(image_url, stream=True)
    with open(os.path.join(FOLDER_NAME, f"shoes_{i+1}.png"), 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

print("Image Download Successfully")