from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    URL = "https://qa-scooter.education-services.ru/"

    ORDER_BUTTONS = (By.XPATH, "//button[normalize-space()='Заказать']")
    FAQ_QUESTIONS = (By.CSS_SELECTOR, ".accordion__button")
    FAQ_ANSWER = (By.CSS_SELECTOR, ".accordion__panel")
    SCOOTER_LOGO = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def click_order_top(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ORDER_BUTTONS)
        )
        self.driver.find_elements(*self.ORDER_BUTTONS)[0].click()

    def click_order_bottom(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTONS)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", buttons[-1]
        )
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTONS))
        self.driver.find_elements(*self.ORDER_BUTTONS)[-1].click()

    def click_faq(self, index):
        questions = self.wait.until(
            EC.presence_of_all_elements_located(self.FAQ_QUESTIONS)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", questions[index]
        )
        questions[index].click()

    def get_faq_answer(self, index):
        answers = self.wait.until(
            EC.presence_of_all_elements_located(self.FAQ_ANSWER)
        )
        return answers[index].text

    def click_scooter_logo(self):
        self.wait.until(EC.element_to_be_clickable(self.SCOOTER_LOGO)).click()

    def click_yandex_logo(self):
        self.wait.until(EC.element_to_be_clickable(self.YANDEX_LOGO)).click()
