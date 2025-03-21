# Import necessary tools
import math
from selenium import webdriver
import  time
from selenium.webdriver.common.by import By
import  pandas as pd
import  os
import  re

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.daraz.com.bd/catalog/?q=pent")
driver.maximize_window()

# Lists to store extracted data
product_name = []
product_link = []
product_image_link = []
product_price = []
total_review = []

# find all product with all pages
total_product_text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div/div/span[1]').text
total_product = int(re.search(r'\d+', total_product_text).group())

# Find all product elements in a single page
all_products = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div')

# Get total number of products per page
total_products_per_page = len(all_products)

# get total page number
total_page = math.ceil(total_product / total_products_per_page)


# Loop throw for page
for page in range(1, total_page+1):
    page_number = str(page)
    driver.get(f'https://www.daraz.com.bd/catalog/?page={page_number}&q=pent&spm=a2a0e.tm80335411.search.d_go')

    # Extract product details
    for i in range(1, total_products_per_page):
        j = str(i)
        try:
            # Extract product name and link
            link_element = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{j}]/div/div/div[2]/div[2]/a')
            link = link_element.get_attribute("href")
            name = link_element.text

            # Extract product image
            image_link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{j}]/div/div/div[1]/div/a/div/img').get_attribute(
                "src")

            # Extract product price
            price_element = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{j}]/div/div/div[2]/div[3]/span')
            price = price_element.text.strip("৳")

            # Extract total reviews
            try:
                reviews_element = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{j}]/div/div/div[2]/div[5]/div/span')
                reviews = reviews_element.text.strip("()")  # Remove parentheses
            except Exception as e:
                print(e)
                reviews = "0"

            # Append to list
            product_name.append(name)
            product_link.append(link)
            product_image_link.append(image_link)
            product_price.append(price)
            total_review.append(reviews)

        except Exception as e:
            print(e)

# Save extract data to csv file
df = pd.DataFrame({
    "product_name": product_name,
    "product_link": product_link,
    "product_image_link": product_image_link,
    "product_price": product_price,
    "product_total_review": total_review
    })

if os.path.exists("products.csv"):
    os.remove('products.csv')

df.to_csv("products.csv", index=False, encoding="utf-8-sig")
print("CSV file save successfully")


# Wait and close browser
time.sleep(20)
driver.quit()
