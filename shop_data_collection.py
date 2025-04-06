from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
import pandas as pd


# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.google.com/maps/search/laptop+shop+mirpur/@23.9173399,90.328726,12z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI1MDQwMi4xIKXMDSoASAFQAw%3D%3D")
driver.refresh()
driver.maximize_window()
time.sleep(2)

# Store shop name and number
shop_info = []
shop_limit = 100

try:
    # Scroll the results panel
    scrollable_div = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')

    while True: # scroll multiple times
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(2)

        # Find all parent elements
        parents = driver.find_elements(By.CLASS_NAME, 'Nv2PK')

        for parent in parents:

            # handle shop name
            try:
                shop_name = parent.find_element(By.CSS_SELECTOR, 'div.qBF1Pd.fontHeadlineSmall').text
            except:
                shop_name = "shop name not found"

            # handle shop phone number
            try:
                shop_number = parent.find_element(By.CLASS_NAME, 'UsdlK').text
            except:
                shop_number = "N/A"

            # Remove duplicates element
            if not any(shop['shop name'] == shop_name and shop['shop number'] == shop_number for shop in shop_info):
                shop_info.append({"shop name": shop_name, "shop number": shop_number})


        if len(shop_info) >= shop_limit:
            break


except Exception as e:
    print(e)

# Create dataframe
df = pd.DataFrame(shop_info)

# Delete old file
filename = "collect-shop-info.csv"
if os.path.exists(filename):
    os.remove(filename)

# Save csv file
df.to_csv("collect-shop-info.csv", index=False, encoding="utf-8-sig")
print("Shop Info Save Successfully")

# Wait for few second to see the result
time.sleep(5)
# close the browser
driver.quit()
