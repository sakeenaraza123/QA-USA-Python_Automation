from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import UrbanRoutesPage
import data
import helpers


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Check if server is reachable before setting up driver
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL.strip()):
            print("Connected to the Urban Routes server")
            options = Options()
            options.add_experimental_option("goog:loggingPrefs", {"performance": "ALL"})
            cls.driver = webdriver.Chrome(options=options)
            cls.wait = WebDriverWait(cls.driver, 10)
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")
            raise Exception("Urban Routes server not reachable.")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

        # Verify the addresses were set correctly
        from_value = self.driver.find_element(*self.page.FROM_INPUT).get_attribute("value")
        to_value = self.driver.find_element(*self.page.TO_INPUT).get_attribute("value")
        assert from_value == data.ADDRESS_FROM
        assert to_value == data.ADDRESS_TO

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.select_supportive_plan()

        # Wait for the plan selection to complete and verify supportive plan is selected
        self.wait.until(lambda driver: "selected" in self.page.get_current_selected_plan())

        # Verify supportive plan is specifically selected
        assert self.page.get_current_selected_plan() == "Supportive"

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.enter_phone(data.PHONE_NUMBER)
        self.page.enter_sms_code()

        # Verify phone verification was successful (next step appears)
        assert self.page.is_card_input_displayed()

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)

        # Verify card was added successfully
        assert self.page.is_card_linked()

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)

        # Verify comment was entered
        comment_value = self.page.get_driver_comment()
        assert data.MESSAGE_FOR_DRIVER in comment_value

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.order_blanket_and_handkerchiefs()

        # Wait for the blanket status element to be present and visible
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='r-sw']//div[@class='switch-input']")
            ))

            # Verify blanket and handkerchiefs are ordered using is_blanket_selected
            assert self.page.is_blanket_selected()
        except:
            # Fallback verification if the element structure is different
            status = self.page.get_blanket_status()
            assert status == "Added" or self.page.is_blanket_selected()

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

        # Order 2 ice creams using a loop
        for i in range(2):
            self.page.add_ice_cream()

        # Verify 2 ice creams were ordered
        ice_cream_count = self.page.get_ice_cream_count()
        assert ice_cream_count == 2

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL.strip())
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.select_supportive_plan()
        self.page.enter_phone(data.PHONE_NUMBER)
        self.page.enter_sms_code()
        self.page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        self.page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)

        # Finalize the order and verify car search modal appears
        modal = self.page.finalize_order()
        assert self.page.is_car_search_modal_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()