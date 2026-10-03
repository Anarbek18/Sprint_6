from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL


class MainPage:
    URL = BASE_URL

    ORDER_BUTTONS = (By.XPATH, "//button[normalize-space()='Заказать']")
    FAQ_QUESTIONS = (By.CSS_SELECTOR, ".accordion__button")
    FAQ_ANSWERS = (By.CSS_SELECTOR, ".accordion__panel")
    SCOOTER_LOGO = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def click_order(self, position):
        """Нажимает на верхнюю или нижнюю кнопку «Заказать»."""
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTONS)
        )

        index = 0 if position == "top" else -1
        button = buttons[index]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        self.wait.until(lambda _: button.is_enabled()).click()

    def click_faq(self, index):
        questions = self.wait.until(
            EC.presence_of_all_elements_located(self.FAQ_QUESTIONS)
        )
        question = questions[index]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", question
        )
        self.wait.until(lambda _: question.is_displayed()).click()

    def get_faq_answer(self, index):
        answers = self.wait.until(
            EC.presence_of_all_elements_located(self.FAQ_ANSWERS)
        )
        return answers[index].text

    def click_scooter_logo(self):
        self.wait.until(EC.element_to_be_clickable(self.SCOOTER_LOGO)).click()

    def is_home_page_opened(self):
        return self.driver.current_url.rstrip("/") == self.URL.rstrip("/")

    def open_yandex_logo_and_get_redirect_url(self):
        """Открывает ссылку Яндекса и возвращает URL нового окна."""
        old_windows = set(self.driver.window_handles)
        self.wait.until(EC.element_to_be_clickable(self.YANDEX_LOGO)).click()

        self.wait.until(
            lambda driver: len(set(driver.window_handles) - old_windows) == 1
        )
        new_window = next(iter(set(self.driver.window_handles) - old_windows))
        self.driver.switch_to.window(new_window)

        self.wait.until(lambda driver: driver.current_url not in ("", "about:blank"))
        return self.driver.current_url
