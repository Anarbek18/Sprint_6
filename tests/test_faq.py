import allure
import pytest

from page_objects.main_page import MainPage


FAQ_DATA = [
    pytest.param(0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой.", id="price_and_payment"),
    pytest.param(1, "Пока что у нас так: один заказ — один самокат.", id="several_scooters"),
    pytest.param(2, "Допустим, вы оформляете заказ на 8 мая.", id="rental_time"),
    pytest.param(3, "Только начиная с завтрашнего дня.", id="order_today"),
    pytest.param(4, "Пока что нет! Но если что-то срочное", id="extend_or_return"),
    pytest.param(5, "Самокат приезжает к вам с полной зарядкой.", id="charger"),
    pytest.param(6, "Да, пока самокат не привезли.", id="cancel_order"),
    pytest.param(7, "Да, обязательно. Всем самокатов!", id="mkad_delivery"),
]


class TestFAQ:
    @allure.title("Проверка ответа на вопрос «О важном»")
    @pytest.mark.parametrize("question_index, expected_answer", FAQ_DATA)
    def test_faq_answer(self, driver, question_index, expected_answer):
        main_page = MainPage(driver)
        main_page.open()
        main_page.click_faq(question_index)

        with allure.step("Проверить текст ответа"):
            actual_answer = main_page.get_faq_answer(question_index)
            assert expected_answer in actual_answer
