import json
from datetime import datetime
from unittest.mock import patch

import pytest

from src.utils import (
    filter_by_date_range,
    get_card_info,
    get_greeting,
    load_transactions_from_excel,
    load_user_settings,
)


# ---------- get_greeting ----------

@pytest.mark.parametrize(
    "hour, expected",
    [
        (6, "Доброе утро"),
        (9, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (15, "Добрый день"),
        (17, "Добрый день"),
        (18, "Добрый вечер"),
        (21, "Добрый вечер"),
        (22, "Добрый вечер"),
        (23, "Доброй ночи"),
        (0, "Доброй ночи"),
        (3, "Доброй ночи"),
        (5, "Доброй ночи"),
    ],
)
def test_get_greeting(hour, expected):
    """Проверяем все временные интервалы."""
    fake_now = datetime(2024, 1, 1, hour, 0, 0)

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fake_now

    with patch("src.utils.datetime", FakeDateTime):
        assert get_greeting() == expected


# ---------- load_transactions_from_excel ----------

def test_load_transactions_from_excel(tmp_path):
    """Проверяем, что функция читает Excel и возвращает список словарей."""
    import pandas as pd

    df = pd.DataFrame({
        "Дата операции": ["31.12.2021 16:44:00", "30.12.2021 12:00:00"],
        "Дата платежа": ["31.12.2021", "31.12.2021"],
        "Номер карты": ["*7197", "*5091"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-160.89, -564.0],
        "Валюта операции": ["RUB", "RUB"],
        "Сумма платежа": [-160.89, -564.0],
        "Валюта платежа": ["RUB", "RUB"],
        "Кэшбэк": [0, 5],
        "Категория": ["Супермаркеты", "Различные товары"],
        "MCC": [5411.0, 5399.0],
        "Описание": ["Колхоз", "Ozon.ru"],
        "Бонусы (включая кэшбэк)": [3.0, 5.0],
        "Округление на инвесткопилку": [0.0, 0.0],
        "Сумма операции с округлением": [160.89, 564.0],
    })

    file_path = tmp_path / "test_operations.xlsx"
    df.to_excel(file_path, index=False)

    result = load_transactions_from_excel(str(file_path))

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["Номер карты"] == "*7197"
    assert result[0]["Сумма операции"] == -160.89
    # Дата приведена к формату YYYY-MM-DD HH:MM:SS
    assert result[0]["Дата операции"].startswith("2021-12-31")


# ---------- get_card_info ----------

@pytest.fixture
def sample_transactions():
    return [
        {"Номер карты": "*7197", "Сумма операции": -100.0, "Кешбэк": 1.0},
        {"Номер карты": "*7197", "Сумма операции": -200.0, "Кешбэк": 2.0},
        {"Номер карты": "*5091", "Сумма операции": -500.0, "Кешбэк": 5.0},
        {"Номер карты": "*7197", "Сумма операции": 1000.0, "Кешбэк": 0.0},  # поступление
        {"Номер карты": "", "Сумма операции": -50.0, "Кешбэк": 0.0},        # без карты
    ]


def test_get_card_info(sample_transactions):
    result = get_card_info(sample_transactions)
    by_card = {c["last_digits"]: c for c in result}

    assert "7197" in by_card
    assert by_card["7197"]["total_spent"] == 300.0
    assert by_card["7197"]["cashback"] == 3.0

    assert "5091" in by_card
    assert by_card["5091"]["total_spent"] == 500.0
    assert by_card["5091"]["cashback"] == 5.0

    # поступления не учитываются в расходах
    assert by_card["7197"]["total_spent"] == 300.0


# ---------- filter_by_date_range ----------

def test_filter_by_date_range():
    tx = [
        {"Дата операции": "2021-12-01 10:00:00"},
        {"Дата операции": "2021-12-15 10:00:00"},
        {"Дата операции": "2021-12-31 10:00:00"},
        {"Дата операции": "2022-01-01 10:00:00"},
    ]
    result = filter_by_date_range(tx, "2021-12-01", "2021-12-31")
    assert len(result) == 3


# ---------- load_user_settings ----------

def test_load_user_settings(tmp_path):
    settings = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    file_path = tmp_path / "user_settings.json"
    file_path.write_text(json.dumps(settings, ensure_ascii=False), encoding="utf-8")

    result = load_user_settings(str(file_path))
    assert result == settings
    assert result["user_currencies"] == ["USD"]
