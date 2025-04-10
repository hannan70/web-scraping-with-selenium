from selenium import webdriver
from selenium.webdriver.common.by import By
import booking.constants as const
import time
from booking.filter_booking import FilterBooking
from booking.booking_report import BookingReport
from selenium.common.exceptions import NoSuchElementException

class Booking(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        super(Booking, self).__init__()
        self.refresh()
        self.maximize_window()

    # After run scripts it's exit the browser
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    # Browse the first page in out target website
    def land_first_page(self):
        self.get(const.BASE_URL)

    # Popup
    def remove_popup(self):
        try:
            popup = self.find_element(By.CSS_SELECTOR, '[data-bui-theme="traveller_ex-light"]')
            popup.click()
        except NoSuchElementException:
            print("No popup found.")
            pass
        except Exception as e:
            pass
            print(f"Unexpected error: {e}")


    # change currency element by clicking
    def change_currency(self, currency=None):
        try:
            currency_element = self.find_element(By.CSS_SELECTOR,
                                                 'button[data-testid="header-currency-picker-trigger"]')
            currency_element.click()
            currency_options = self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
            for option in currency_options:
                if currency.lower() in option.text.lower():
                    option.click()
                    break
        except Exception as e:
            print(e)

    # search box select place
    def select_place(self, place_name):
        try:
            # Go to search field and write place name
            search_element = self.find_element(By.NAME, 'ss')
            search_element.clear()
            search_element.send_keys(place_name)
            time.sleep(3)
            # After searchin click the first result
            first_element = self.find_element(By.ID, 'autocomplete-result-0')
            first_element.click()
        except Exception as e:
            print(e)

    # select data field
    def select_datas(self, check_in_data, check_out_date):
       try:
           check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_data}"]')
           check_in_element.click()
           check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
           check_out_element.click()
       except Exception as e:
           print(e)


    # Select adult counter
    def select_adults(self, count):
        try:
            selected_elements = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
            selected_elements.click()

            # Decrease the adult number
            while True:
                decrease_adult_element = self.find_element(By.XPATH, '//*[@id=":ri:"]/div/div[1]/div[2]/button[1]')
                decrease_adult_element.click()

                adult_value = self.find_element(By.ID, 'group_adults')
                value = adult_value.get_attribute('value')

                if int(value) == 1:
                    break

            # increase the adult number
            for _ in range(1, count):
                increase_adult_element = self.find_element(By.XPATH, '//*[@id=":ri:"]/div/div[1]/div[2]/button[2]')
                increase_adult_element.click()
        except Exception as e:
            print(e)


    # Search booking
    def search_booking(self):
        try:
            search = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search.click()
        except Exception as e:
            print(e)

    def filter_booking(self):
        filter = FilterBooking(driver=self)
        filter.apply_star_filter(2)
        filter.bed_preference("Twin beds", "Double bed")
        filter.price_filter()

    def booking_report(self):
        report = BookingReport(driver=self)
        report.booking_report_collect()
        report.save_collection_file()














