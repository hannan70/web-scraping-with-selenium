import time
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver # for code suggestion
from selenium.webdriver.common.by import By

class FilterBooking:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    # filter all hotel using bet preference
    def bed_preference(self, *bed_names):
        try:
            bed_parents_elements = self.driver.find_element(By.CSS_SELECTOR, '[data-filters-group="tdb"]')
            bed_child_elements = bed_parents_elements.find_elements(By.CSS_SELECTOR, '*')

            for bed_name in bed_names:
                for bed_child_element in bed_child_elements:
                    if str(bed_child_element.get_attribute("innerHTML")).strip() == bed_name:
                        bed_child_element.click()
                        time.sleep(2)
        except Exception as e:
            print(e)

    # filter all hotel using star
    def apply_star_filter(self, *star_values):
       try:
           # Parent class
           star_filter_box = self.driver.find_element(By.CSS_SELECTOR, '[data-filters-group="class"]')
           # All child class
           star_child_elements = star_filter_box.find_elements(By.CSS_SELECTOR, '*')

           for star_value in star_values:
               for star_element in star_child_elements:
                   if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                       star_element.click()
                       time.sleep(2)
       except Exception as e:
           print(e)

    # filter all hotel using price
    def price_filter(self):
        time.sleep(3)
        try:
            slider_handles = self.driver.find_elements(By.CSS_SELECTOR, '.b18036920b')
            min_slider = slider_handles[0]
            max_slider = slider_handles[1]

            time.sleep(2)
            actions = ActionChains(self.driver)
            actions.drag_and_drop_by_offset(min_slider, 50, 0).release().perform()
            time.sleep(2)
            actions.drag_and_drop_by_offset(max_slider, -60, 0).release().perform()
            time.sleep(2)
        except Exception as e:
            print(e)






