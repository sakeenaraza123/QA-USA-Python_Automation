from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helpers
import time

class UrbanRoutesPage:
    # LOCATORS
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    SUPPORTIVE_PLAN = (By.XPATH, "//div[contains(text(),'Ice cream')]/ancestor::div[contains(@id, 'tariff-card')]")
    PHONE_INPUT = (By.ID, "phone-input")
    SEND_CODE_BTN = (By.ID, "send-code-btn")
    SMS_CODE_INPUT = (By.ID, "code")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CVV_INPUT = (By.ID, "code")
    LINK_CARD_BTN = (By.ID, "link-card-btn")
    DRIVER_COMMENT_INPUT = (By.ID, "driver-comment")
    BLANKET_TOGGLE = (By.ID, "extra-blanket")
    BLANKET_STATUS = (By.ID, "blanket-status")
    ICE_CREAM_BTN = (By.ID, "icecream-btn")
    ORDER_BTN = (By.ID, "book-supportive")
    SEARCH_MODAL = (By.ID, "search-modal")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_address(self, address_from, address_to):
        self.driver.find_element(*self.FROM_INPUT).send_keys(address_from)
        self.driver.find_element(*self.TO_INPUT).send_keys(address_to)

    def select_supportive_plan(self):
        button = self.driver.find_element(*self.SUPPORTIVE_PLAN)
        if "selected" not in button.get_attribute("class"):
            button.click()

    def enter_phone(self, phone):
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)
        self.driver.find_element(*self.SEND_CODE_BTN).click()

    def enter_sms_code(self):
        code = helpers.retrieve_phone_code(self.driver)
        self.driver.find_element(*self.SMS_CODE_INPUT).send_keys(code)

    def add_credit_card(self, number, cvv):
        self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(number)
        cvv_input = self.driver.find_element(*self.CVV_INPUT)
        cvv_input.send_keys(cvv)
        cvv_input.send_keys(Keys.TAB)
        time.sleep(1)
        self.driver.find_element(*self.LINK_CARD_BTN).click()

    def leave_driver_comment(self, comment):
        self.driver.find_element(*self.DRIVER_COMMENT_INPUT).send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_TOGGLE).click()

    def get_blanket_status(self):
        return self.driver.find_element(*self.BLANKET_STATUS).text

    def order_ice_cream(self, count=2):
        for _ in range(count):
            self.driver.find_element(*self.ICE_CREAM_BTN).click()

    def finalize_order(self, comment):
        self.driver.find_element(*self.DRIVER_COMMENT_INPUT).send_keys(comment)
        self.driver.find_element(*self.ORDER_BTN).click()
        return self.wait.until(EC.visibility_of_element_located(self.SEARCH_MODAL))
