# import all necessary tools
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# load csv file
data = pd.read_csv("users.csv")

# Initialize webdriver
driver = webdriver.Chrome()
driver.refresh()
driver.maximize_window()


# get each row name and email in the csv file
for index, row in data.iterrows():
    driver.get("https://forms.gle/B2V7sUXzmBbqtdk68")
    time.sleep(2)
    try:
        name = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        email = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')

        # Fill the form fields
        name.send_keys(row['name'])
        time.sleep(2)
        email.send_keys( row['email'])
        time.sleep(2)

        # Submit Form
        submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit_btn.click()
        print("Form submit successfully")
        time.sleep(2)

    except Exception as e:
        print(e)

time.sleep(20)
driver.quit()