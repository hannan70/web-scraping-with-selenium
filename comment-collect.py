# import all necessary tools
from selenium import  webdriver
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd

from selenium.webdriver.common.print_page_options import PrintOptions

# initialize Webdriver
driver = webdriver.Chrome()
driver.get("https://www.daraz.com.bd/products/bata-i328811880-s1604199994.html")
driver.refresh()
driver.maximize_window()

# List to store extract comments
product_comments = []

# Get the height of the comment section
comment_section = driver.find_element(By.XPATH, '//*[@id="block-YtFoiQEVZb4"]')
comment_section_height = driver.execute_script("return arguments[0].scrollHeight;", comment_section)
driver.execute_script("arguments[0].scrollIntoView();", comment_section)
time.sleep(5)


for i in range(comment_section_height, comment_section_height+1000 , 50):
    driver.execute_script(f"window.scrollTo(0, {i})")
    time.sleep(2)

for i in range(1, 6):
    comments = driver.find_element(By.XPATH, f'//*[@id="module_product_review"]/div/div/div[3]/div[1]/div[{i}]/div[3]/div[1]')
    product_comments.append(comments.text)

# Save extract data to csv file
df = pd.DataFrame({
    "product_comments": product_comments,
    })

if os.path.exists("comments.csv"):
    os.remove('comments.csv')

df.to_csv("comments.csv", index=False, encoding="utf-8-sig")
print("CSV file save successfully")


time.sleep(20)
driver.quit()