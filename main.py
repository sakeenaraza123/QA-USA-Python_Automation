from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import data
import helpers
from pages import UrbanRoutesPage  # NEW

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL.strip()):
            cls.driver.get(data.URBAN_ROUTES_URL.strip())
            cls.page = UrbanRoutesPage(cls.driver)  # REUSABLE
        else:
            raise Exception("Urban Routes server not reachable.")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)

    def test_select_plan(self):
        self.page.select_supportive_plan()

    def test_fill_phone_number(self):
        self.page.enter_phone(data.PHONE_NUMBER)
        self.page.enter_sms_code()

    def test_fill_card(self):
        self.page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)

    def test_comment_for_driver(self):
        self.page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)

    def test_order_blanket_and_handkerchiefs(self):
        self.page.order_blanket_and_handkerchiefs()

    def test_order_2_ice_creams(self):
        self.page.order_ice_cream(count=2)

    def test_car_search_model_appears(self):
        self.page.finalize_order(data.MESSAGE_FOR_DRIVER)
