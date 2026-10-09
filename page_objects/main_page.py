from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL
from page_objects.base_page import BasePage


class MainPage(BasePage):
    URL = BASE_URL

    ORDER_BUTTONS = (By.XPATH, "//button[normalize-space()='Заказать']")
    FAQ_QUESTIONS = (By.CSS_SELECTOR, ".accordion__button")
    FAQ_ANSWER = (By.CSS_SELECTOR, ".accordion__panel")
    SCOOTER_LOGO = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")

    def open(self):
        self.go_to_url(self.URL)

    def click_order_top(self):
        buttons = self.find_elements(self.ORDER_BUTTONS)
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTONS))
        buttons[0].click()

    def click_order_bottom(self):
        buttons = self.find_elements(self.ORDER_BUTTONS)
        button = buttons[-1]
        self.scroll_to_element(button)
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTONS))
        self.find_elements(self.ORDER_BUTTONS)[-1].click()

    def click_faq(self, index):
        questions = self.find_elements(self.FAQ_QUESTIONS)
        question = questions[index]
        self.scroll_to_element(question)
        question.click()

    def get_faq_answer(self, index):
        return self.find_elements(self.FAQ_ANSWER)[index].text

    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)
