
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import pandas as pd
import os

class BookingReport:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.report = []


    def booking_report_collect(self):

        booking_items = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')

        for booking_item in booking_items:
            # collect the hotel name
            try:
                hotel_name = booking_item.find_element(By.CSS_SELECTOR, '[data-testid="title"]').text
                print(hotel_name)
            except Exception as e:
                hotel_name = "N/A"

            # collect the hotel score
            try:
                score = booking_item.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"] .a3b8729ab1').text
                score = score.split()[1]
            except:
                score = "N/A"

            # collect the hotel price
            try:
                hotel_price = booking_item.find_element(By.CSS_SELECTOR, '[data-testid="price-and-discounted-price"]').text
            except:
                hotel_price = 'N/A'

            self.report.append({"hotel name": hotel_name, "hotel price" : hotel_price, "hotel score": score})


    def save_collection_file(self):
        # Create dataframe
        df = pd.DataFrame(self.report)

        # Delete old file
        filename = "hotel_info.csv"
        if os.path.exists(filename):
            os.remove(filename)

        # Save csv file
        df.to_csv("hotel_info.csv", index=False, encoding="utf-8-sig")
        print("Hotel Info Save Successfully")