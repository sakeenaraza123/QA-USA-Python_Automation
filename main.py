from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage
import data
import helpers

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(data.URBAN_ROUTES_URL.strip())
        cls.page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        from_value = self.driver.find_element(*self.page.FROM_INPUT).get_attribute("value")
        to_value = self.driver.find_element(*self.page.TO_INPUT).get_attribute("value")
        assert from_value == data.ADDRESS_FROM
        assert to_value == data.ADDRESS_TO

    def test_select_tariff(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.select_supportive_plan()
        assert "selected" in self.page.get_current_selected_plan()

    def test_phone_verification(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.enter_phone(data.PHONE_NUMBER)
        self.page.enter_sms_code()
        assert self.page.driver.find_element(*self.page.CARD_NUMBER_INPUT).is_displayed()

    def test_card_entry(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.driver.find_element(*self.page.LINK_CARD_BTN).is_displayed()

    def test_driver_comment(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)
        comment_box = self.page.driver.find_element(*self.page.DRIVER_COMMENT_INPUT)
        assert data.MESSAGE_FOR_DRIVER in comment_box.get_attribute("value")

    def test_extras(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.order_blanket_and_handkerchiefs()
        status = self.page.get_blanket_status()
        assert status == "Added"
        self.page.order_ice_cream(count=2)

    def test_finalize_booking(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        modal = self.page.finalize_order(data.MESSAGE_FOR_DRIVER)
        assert modal.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
