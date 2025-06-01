from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import helpers


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators (selectors)
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(), 'Call a taxi')]")

    # Tariff selection
    SUPPORTIVE_PLAN = (By.XPATH, "//div[@class='tcard-title' and text()='Supportive']")
    SELECTED_PLAN = (By.CSS_SELECTOR, ".tcard.active")

    # Phone number
    PHONE_NUMBER_BUTTON = (By.CLASS_NAME, "np-button")
    PHONE_NUMBER_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Next')]")
    SMS_CODE_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm')]")

    # Payment method
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-button")
    ADD_CARD_BUTTON = (By.XPATH, "//div[contains(text(), 'Add card')]")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.XPATH, "//input[@placeholder='12']")
    LINK_CARD_BUTTON = (By.XPATH, "//button[contains(text(), 'Link')]")
    CLOSE_PAYMENT_MODAL = (By.XPATH, "//button[@class='close-button section-close']")

    # Driver comment
    DRIVER_COMMENT_INPUT = (By.ID, "comment")

    # Blanket and handkerchiefs
    BLANKET_CHECKBOX = (By.XPATH, "//div[@class='r-sw']//div[@class='switch']")
    BLANKET_STATUS = (By.XPATH, "//div[@class='r-sw']//div[@class='switch-input']")

    # Ice cream
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//div[@class='counter-plus']")
    ICE_CREAM_COUNTER = (By.XPATH, "//div[@class='counter-value']")

    # Final order
    ORDER_TAXI_BUTTON = (By.XPATH, "//button[contains(@class, 'smart-button') and contains(text(), 'Order')]")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[@class='order-header-title' and contains(text(), 'Car search')]")

    def set_route(self, from_address, to_address):
        """Set the from and to addresses"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.FROM_INPUT))

        from_field = self.driver.find_element(*self.FROM_INPUT)
        from_field.clear()
        from_field.send_keys(from_address)

        to_field = self.driver.find_element(*self.TO_INPUT)
        to_field.clear()
        to_field.send_keys(to_address)

        # Click call taxi button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def select_supportive_plan(self):
        """Select the Supportive tariff plan"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN))
        self.driver.find_element(*self.SUPPORTIVE_PLAN).click()

    def get_current_selected_plan(self):
        """Get the class attribute of currently selected plan"""
        selected_element = self.driver.find_element(*self.SELECTED_PLAN)
        return selected_element.get_attribute("class")

    def enter_phone(self, phone_number):
        """Enter phone number"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PHONE_NUMBER_BUTTON))
        self.driver.find_element(*self.PHONE_NUMBER_BUTTON).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PHONE_NUMBER_INPUT))
        phone_input = self.driver.find_element(*self.PHONE_NUMBER_INPUT)
        phone_input.clear()
        phone_input.send_keys(phone_number)

        self.driver.find_element(*self.NEXT_BUTTON).click()

    def enter_sms_code(self):
        """Enter SMS verification code"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SMS_CODE_INPUT))

        # Get the SMS code using helper function
        code = helpers.retrieve_phone_code(self.driver)

        sms_input = self.driver.find_element(*self.SMS_CODE_INPUT)
        sms_input.send_keys(code)

        self.driver.find_element(*self.CONFIRM_BUTTON).click()

    def is_card_input_displayed(self):
        """Check if card input is displayed (phone verification successful)"""
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.PAYMENT_METHOD_BUTTON))
            return True
        except:
            return False

    def add_credit_card(self, card_number, card_code):
        """Add credit card information"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON))
        self.driver.find_element(*self.PAYMENT_METHOD_BUTTON).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON))
        self.driver.find_element(*self.ADD_CARD_BUTTON).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CARD_NUMBER_INPUT))
        card_input = self.driver.find_element(*self.CARD_NUMBER_INPUT)
        card_input.send_keys(card_number)

        code_input = self.driver.find_element(*self.CARD_CODE_INPUT)
        code_input.send_keys(card_code)

        # Click outside to lose focus, then link card
        self.driver.find_element(*self.CARD_NUMBER_INPUT).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.LINK_CARD_BUTTON))
        self.driver.find_element(*self.LINK_CARD_BUTTON).click()

        # Close payment modal
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CLOSE_PAYMENT_MODAL))
        self.driver.find_element(*self.CLOSE_PAYMENT_MODAL).click()

    def is_card_linked(self):
        """Check if card was successfully linked"""
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON))
            return True
        except:
            return False

    def leave_driver_comment(self, message):
        """Leave a comment for the driver"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.DRIVER_COMMENT_INPUT))
        comment_input = self.driver.find_element(*self.DRIVER_COMMENT_INPUT)
        comment_input.send_keys(message)

    def get_driver_comment(self):
        """Get the driver comment value"""
        comment_input = self.driver.find_element(*self.DRIVER_COMMENT_INPUT)
        return comment_input.get_attribute("value")

    def order_blanket_and_handkerchiefs(self):
        """Order blanket and handkerchiefs"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BLANKET_CHECKBOX))
        self.driver.find_element(*self.BLANKET_CHECKBOX).click()

    def get_blanket_status(self):
        """Get blanket order status"""
        status_element = self.driver.find_element(*self.BLANKET_STATUS)
        if status_element.is_selected():
            return "Added"
        return "Not Added"

    def is_blanket_selected(self):
        """Check if blanket is selected"""
        checkbox = self.driver.find_element(*self.BLANKET_STATUS)
        return checkbox.is_selected()

    def add_ice_cream(self):
        """Add one ice cream"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
        self.driver.find_element(*self.ICE_CREAM_PLUS_BUTTON).click()

    def get_ice_cream_count(self):
        """Get the number of ice creams ordered"""
        counter_element = self.driver.find_element(*self.ICE_CREAM_COUNTER)
        return int(counter_element.text)

    def finalize_order(self):
        """Finalize the taxi order"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ORDER_TAXI_BUTTON))
        self.driver.find_element(*self.ORDER_TAXI_BUTTON).click()

    def is_car_search_modal_displayed(self):
        """Check if car search modal is displayed"""
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.CAR_SEARCH_MODAL))
            return True
        except:
            return False