import allure
import pytest

from page_objects.main_page import MainPage


FAQ_DATA = [
    (
        0,
        "Сутки — 400 рублей. Оплата курьеру — наличными или картой."
    ),
    (
        1,
        "Пока что у нас так: один заказ — один самокат."
    ),
    (
        2,
        "Допустим, вы оформляете заказ на 8 мая."
    ),
    (
        3,
        "Только начиная с завтрашнего дня."
    ),
    (
        4,
        "Пока что нет! Но если что-то срочное"
    ),
    (
        5,
        "Самокат приезжает к вам с полной зарядкой."
    ),
    (
        6,
        "Да, пока самокат не привезли."
    ),
    (
        7,
        "Да, обязательно. Всем самокатов!"
    ),
]


class TestFAQ:

    @allure.title("Проверка ответа FAQ")
    @pytest.mark.parametrize("question_index, expected_answer", FAQ_DATA)
    def test_faq_answer(self, driver, question_index, expected_answer):
        page = MainPage(driver)
        page.open()

        page.click_faq(question_index)

        with allure.step("Проверить текст ответа"):
            actual_answer = page.get_faq_answer(question_index)
            assert expected_answer in actual_answer
