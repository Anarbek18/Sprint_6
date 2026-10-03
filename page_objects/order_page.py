from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrderPage:
    NAME = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.CSS_SELECTOR, ".select-search__input")
    PHONE = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[normalize-space()='Далее']")

    DATE_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Когда привезти самокат')]")
    RENTAL_PERIOD = (By.XPATH, "//*[contains(@class,'Dropdown-control')]")
    BLACK_COLOR = (By.ID, "black")
    GREY_COLOR = (By.ID, "grey")
    COMMENT = (
        By.XPATH,
        "//input[contains(@placeholder, 'Комментарий')] | "
        "//textarea[contains(@placeholder, 'Комментарий')]",
    )
    ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Заказать']")
    CONFIRM_ORDER = (By.XPATH, "//button[normalize-space()='Да']")
    SUCCESS_MODAL = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Заказ оформлен')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _fill(self, locator, value):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def is_first_step_opened(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.NAME)
        ).is_displayed()

    def fill_first_step(self, name, surname, address, metro, phone):
        self._fill(self.NAME, name)
        self._fill(self.SURNAME, surname)
        self._fill(self.ADDRESS, address)

        metro_input = self.wait.until(
            EC.element_to_be_clickable(self.METRO_INPUT)
        )
        metro_input.click()
        metro_input.send_keys(metro)

        metro_option = (
            By.XPATH,
            f"//*[contains(@class,'select-search__row') and "
            f"normalize-space()='{metro}']",
        )
        self.wait.until(EC.element_to_be_clickable(metro_option)).click()
        self._fill(self.PHONE, phone)
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def fill_second_step(self, date, rental_period, color, comment="Не звонить"):
        self._fill(self.DATE_INPUT, date)

        self.wait.until(EC.element_to_be_clickable(self.RENTAL_PERIOD)).click()
        rental_option = (
            By.XPATH,
            f"//*[contains(@class,'Dropdown-option') and "
            f"normalize-space()='{rental_period}']",
        )
        self.wait.until(EC.element_to_be_clickable(rental_option)).click()

        color_locator = {
            "black": self.BLACK_COLOR,
            "grey": self.GREY_COLOR,
        }[color]
        self.wait.until(EC.element_to_be_clickable(color_locator)).click()

        if self.driver.find_elements(*self.COMMENT):
            self._fill(self.COMMENT, comment)

    def submit_order(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTON)
        )
        button = buttons[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        self.wait.until(lambda _: button.is_enabled()).click()
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_ORDER)).click()

    def is_order_created(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SUCCESS_MODAL)
        ).is_displayed()
