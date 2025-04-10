from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

# Initialize webdriver
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
driver.refresh()
driver.maximize_window()
time.sleep(20)

MEMBER_LIST_LIMIT = 360
member_info = []

# search group name
group_name = "Job & Freelancing (Innovative Skills)"
search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
search_box.send_keys(group_name)
time.sleep(2)

# click the grop name
group = driver.find_element(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div/div[2]')
group.click()
time.sleep(2)

# Click then group name header
header = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]')
header.click()
time.sleep(2)

# view all members
view = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/span/div/span/div/div/div/section/div[6]/div[2]/div[3]/div[2]')
view.click()
time.sleep(2)

# scroll and collect the members name and phone
scrollable_div = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]')


for _ in range(50):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 200", scrollable_div)
    time.sleep(1)

    # collect the name
    members = driver.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div')

    for member in members:

        # Collect phone number
        try:
            phone_number = member.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[4]/div/div/div[2]/div[2]/div[2]/span[1]/span').text
        except:
            phone_number = "N/A"

        # Collect name
        try:
            name = member.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[10]/div/div/div[2]/div[1]/div/div/div/span').text
        except:
            name = "N/A"

        member_info.append({"name": name, "phone": phone_number})



# create filename
filename = "whatsapp-info.csv"

# create dataset
df = pd.DataFrame(member_info)

# remove old existing file
if os.path.exists(filename):
    os.remove(filename)

# Save csv file
df.to_csv("whatsapp-info.csv", index=False, encoding="utf-8-sig")
print("Whatsapp Info Save Successfully")


time.sleep(20)
driver.quit()
