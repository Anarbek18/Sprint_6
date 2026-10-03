# Sprint 6 — Яндекс Самокат

Проект автотестов учебного сервиса Яндекс Самокат.

## Структура

- `page_objects/` — Page Object классы.
- `tests/` — автотесты.
- `conftest.py` — fixture Selenium WebDriver.
- `requirements.txt` — внешние зависимости.

## Установка

CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Для проекта нужен Mozilla Firefox.

## Запуск тестов

```cmd
python -m pytest -v
```

## Allure

Собрать результаты:

```cmd
python -m pytest -v --alluredir=allure_results
```

Открыть отчёт, если Allure Commandline добавлен в PATH:

```cmd
allure serve allure_results
```

## Примечание

Локаторы и тексты основаны на HTML учебного сервиса из задания. Если учебный стенд обновит верстку, локаторы конкретных полей могут потребовать обновления.
