from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from pages import UrbanRoutesPage
import data
import helpers


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL.strip()):
            cls.driver.get(data.URBAN_ROUTES_URL.strip())
            cls.page = UrbanRoutesPage(cls.driver)
        else:
            raise Exception("Urban Routes server not reachable.")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)

    def test_select_tariff(self):
        self.page.select_supportive_plan()
        selected_class = self.page.driver.find_element(*self.page.SUPPORTIVE_PLAN).get_attribute("class")
        assert "selected" in selected_class

    def test_phone_verification(self):
        self.page.enter_phone(data.PHONE_NUMBER)
        self.page.enter_sms_code()
        assert self.page.driver.find_element(*self.page.CARD_NUMBER_INPUT).is_displayed()

    def test_card_entry(self):
        self.page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.driver.find_element(*self.page.LINK_CARD_BTN).is_displayed()

    def test_driver_comment(self):
        self.page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)
        comment_box = self.page.driver.find_element(*self.page.DRIVER_COMMENT_INPUT)
        assert data.MESSAGE_FOR_DRIVER in comment_box.get_attribute("value")

    def test_extras(self):
        self.page.order_blanket_and_handkerchiefs()
        status = self.page.get_blanket_status()
        assert status == "Added"

        self.page.order_ice_cream(count=2)

    def test_finalize_booking(self):
        modal = self.page.finalize_order(data.MESSAGE_FOR_DRIVER)
        assert modal.is_displayed()
