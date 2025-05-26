from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helpers
import time

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_address(self, address_from, address_to):
        self.driver.find_element(By.ID, "from").send_keys(address_from)
        self.driver.find_element(By.ID, "to").send_keys(address_to)

    def select_supportive_plan(self):
        supportive_card = self.driver.find_element(
            By.XPATH, "//div[contains(text(),'Ice cream')]/ancestor::div[contains(@id, 'tariff-card')]"
        )
        if "selected" not in supportive_card.get_attribute("class"):
            supportive_card.click()

    def enter_phone(self, phone):
        self.driver.find_element(By.ID, "phone-input").send_keys(phone)
        self.driver.find_element(By.ID, "send-code-btn").click()

    def enter_sms_code(self):
        code = helpers.retrieve_phone_code(self.driver)
        self.driver.find_element(By.ID, "code").send_keys(code)

    def add_credit_card(self, number, cvv):
        self.driver.find_element(By.ID, "number").send_keys(number)
        cvv_input = self.driver.find_element(By.ID, "code")
        cvv_input.send_keys(cvv)
        cvv_input.send_keys(Keys.TAB)
        time.sleep(1)
        self.driver.find_element(By.ID, "link-card-btn").click()

    def leave_driver_comment(self, comment):
        self.driver.find_element(By.ID, "driver-comment").send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(By.ID, "extra-blanket").click()
        state = self.driver.find_element(By.ID, "blanket-status").text
        assert state == "Added"

    def order_ice_cream(self, count=2):
        for _ in range(count):
            self.driver.find_element(By.ID, "icecream-btn").click()

    def finalize_order(self, comment):
        self.driver.find_element(By.ID, "driver-comment").send_keys(comment)
        self.driver.find_element(By.ID, "book-supportive").click()
        modal = self.wait.until(EC.visibility_of_element_located((By.ID, "search-modal")))
        assert modal.is_displayed()
