from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from page_objects.base_page import BasePage


class OrderPage(BasePage):
    NAME = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.CSS_SELECTOR, ".select-search__input")
    METRO_OPTION = (By.CSS_SELECTOR, ".select-search__row")
    PHONE = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[normalize-space()='Далее']")

    DATE_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Когда привезти самокат')]")
    RENTAL_PERIOD = (By.XPATH, "//*[contains(@class,'Dropdown-control')]")
    RENTAL_OPTIONS = (By.XPATH, "//*[contains(@class,'Dropdown-option')]")

    BLACK_COLOR = (By.ID, "black")
    GREY_COLOR = (By.ID, "grey")
    COMMENT = (By.XPATH, "//input[contains(@placeholder, 'Комментарий')] | //textarea[contains(@placeholder, 'Комментарий')]")

    ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Заказать']")
    CONFIRM_ORDER = (By.XPATH, "//button[normalize-space()='Да']")

    SUCCESS_MODAL = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Заказ оформлен')]"
    )

    def _fill(self, locator, value):
        self.fill_input(locator, value)

    def fill_first_step(self, name, surname, address, metro, phone):
        self._fill(self.NAME, name)
        self._fill(self.SURNAME, surname)
        self._fill(self.ADDRESS, address)

        metro_input = self.wait.until(
            EC.element_to_be_clickable(self.METRO_INPUT)
        )
        metro_input.click()
        metro_input.send_keys(metro)

        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(@class,'select-search__row') and normalize-space()='{metro}']")
            )
        )
        option.click()

        self._fill(self.PHONE, phone)

        self.wait.until(
            EC.element_to_be_clickable(self.NEXT_BUTTON)
        ).click()

    def fill_second_step(self, date, rental_period, color="black", comment="Не звонить"):
        self._fill(self.DATE_INPUT, date)

        self.wait.until(
            EC.element_to_be_clickable(self.RENTAL_PERIOD)
        ).click()

        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(@class,'Dropdown-option') and normalize-space()='{rental_period}']")
            )
        )
        option.click()

        color_locator = self.BLACK_COLOR if color == "black" else self.GREY_COLOR
        self.wait.until(
            EC.element_to_be_clickable(color_locator)
        ).click()

        try:
            self._fill(self.COMMENT, comment)
        except Exception:
                                                                         
                                           
            pass

    def submit_order(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTON)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", buttons[-1]
        )
        self.driver.find_elements(*self.ORDER_BUTTON)[-1].click()

        self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_ORDER)
        ).click()

    def is_order_created(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SUCCESS_MODAL)
        ).is_displayed()
