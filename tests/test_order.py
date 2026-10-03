from datetime import date, timedelta

import allure
import pytest

from page_objects.main_page import MainPage
from page_objects.order_page import OrderPage


ORDER_DATA = [
    pytest.param(
        "Анарбек",
        "Иванов",
        "Москва, улица Ленина, дом 1",
        "Черкизовская",
        "+79991234567",
        "сутки",
        "black",
        id="black_scooter",
    ),
    pytest.param(
        "Иван",
        "Петров",
        "Москва, улица Пушкина, дом 10",
        "Сокольники",
        "+79997654321",
        "двое суток",
        "grey",
        id="grey_scooter",
    ),
]


class TestOrder:
    @allure.title("Заказ самоката: позитивный сценарий")
    @pytest.mark.parametrize("button_position", ["top", "bottom"])
    @pytest.mark.parametrize(
        "name, surname, address, metro, phone, rental_period, color",
        ORDER_DATA,
    )
    def test_create_order(
        self,
        driver,
        button_position,
        name,
        surname,
        address,
        metro,
        phone,
        rental_period,
        color,
    ):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.open()
        main_page.click_order(button_position)
        assert order_page.is_first_step_opened()

        order_page.fill_first_step(name, surname, address, metro, phone)

        tomorrow = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
        order_page.fill_second_step(tomorrow, rental_period, color)
        order_page.submit_order()

        with allure.step("Проверить сообщение об успешном заказе"):
            assert order_page.is_order_created()

    @allure.title("Логотип Самоката возвращает на главную страницу")
    def test_scooter_logo(self, driver):
        main_page = MainPage(driver)
        main_page.open()
        main_page.click_scooter_logo()

        assert main_page.is_home_page_opened()

    @allure.title("Логотип Яндекса открывается в новом окне")
    def test_yandex_logo(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        redirect_url = main_page.open_yandex_logo_and_get_redirect_url()

        assert "dzen.ru" in redirect_url or "dzen" in redirect_url.lower()
