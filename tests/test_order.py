from datetime import date, timedelta

import allure
import pytest

from page_objects.main_page import MainPage
from page_objects.order_page import OrderPage


ORDER_DATA = [
    (
        "Анарбек",
        "Иванов",
        "Москва, улица Ленина, дом 1",
        "Черкизовская",
        "+79991234567",
        "сутки",
        "black",
    ),
    (
        "Иван",
        "Петров",
        "Москва, улица Пушкина, дом 10",
        "Сокольники",
        "+79997654321",
        "двое суток",
        "grey",
    ),
]


class TestOrder:

    @allure.title("Заказ самоката: позитивный сценарий")
    @pytest.mark.parametrize(
        "name, surname, address, metro, phone, rental_period, color",
        ORDER_DATA,
    )
    def test_create_order(
        self,
        driver,
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
        main_page.click_order_top()

        order_page.fill_first_step(
            name, surname, address, metro, phone
        )

        tomorrow = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
        order_page.fill_second_step(
            tomorrow,
            rental_period,
            color,
        )

        order_page.submit_order()

        with allure.step("Проверить сообщение об успешном заказе"):
            assert order_page.is_order_created()

    @allure.title("Кнопки «Заказать» открывают форму заказа")
    @pytest.mark.parametrize("button_position", ["top", "bottom"])
    def test_order_entry_points(self, driver, button_position):
        main_page = MainPage(driver)
        main_page.open()

        if button_position == "top":
            main_page.click_order_top()
        else:
            main_page.click_order_bottom()

        assert driver.current_url == MainPage.URL
        assert driver.find_element(*OrderPage.NAME).is_displayed()

    @allure.title("Логотип Самоката возвращает на главную страницу")
    def test_scooter_logo(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        main_page.click_scooter_logo()

        assert driver.current_url.rstrip("/") == MainPage.URL.rstrip("/")

    @allure.title("Логотип Яндекса открывается в новом окне")
    def test_yandex_logo(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        old_window = driver.current_window_handle
        old_windows = driver.window_handles

        main_page.click_yandex_logo()

        WebDriverWait = __import__(
            "selenium.webdriver.support.ui",
            fromlist=["WebDriverWait"]
        ).WebDriverWait
        WebDriverWait(driver, 10).until(
            lambda d: len(d.window_handles) > len(old_windows)
        )

        new_window = next(
            window for window in driver.window_handles
            if window != old_window
        )
        driver.switch_to.window(new_window)

        assert "dzen.ru" in driver.current_url or "dzen" in driver.current_url.lower()
