from datetime import datetime
from unittest.mock import patch

import pytest

from src.views import get_main_page_view, get_top_transactions


@pytest.fixture
def sample_transactions():
    return [
        {
            "Дата операции": "2024-06-15 12:00:00",
            "Сумма операции": -100.0,
            "Категория": "Супермаркеты",
            "Описание": "Магнит",
            "Номер карты": "*7197",
            "Кешбэк": 1.0,
        },
        {
            "Дата операции": "2024-06-16 12:00:00",
            "Сумма операции": -5000.0,
            "Категория": "Электроника",
            "Описание": "DNS",
            "Номер карты": "*7197",
            "Кешбэк": 50.0,
        },
        {
            "Дата операции": "2024-06-17 12:00:00",
            "Сумма операции": -250.0,
            "Категория": "Фастфуд",
            "Описание": "KFC",
            "Номер карты": "*5091",
            "Кешбэк": 2.5,
        },
        {
            "Дата операции": "2024-06-18 12:00:00",
            "Сумма операции": -1200.0,
            "Категория": "Одежда",
            "Описание": "Wildberries",
            "Номер карты": "*5091",
            "Кешбэк": 12.0,
        },
        {
            "Дата операции": "2024-06-19 12:00:00",
            "Сумма операции": -300.0,
            "Категория": "Аптеки",
            "Описание": "Аптека Вита",
            "Номер карты": "*7197",
            "Кешбэк": 3.0,
        },
        {
            "Дата операции": "2024-06-20 12:00:00",
            "Сумма операции": -80.0,
            "Категория": "Транспорт",
            "Описание": "Метро",
            "Номер карты": "*5091",
            "Кешбэк": 0.5,
        },
    ]


# ---------- get_top_transactions ----------

def test_get_top_transactions_returns_5(sample_transactions):
    result = get_top_transactions(sample_transactions, n=5)
    assert len(result) == 5


def test_get_top_transactions_sorted_desc(sample_transactions):
    result = get_top_transactions(sample_transactions, n=5)
    amounts = [abs(t["amount"]) for t in result]
    assert amounts == sorted(amounts, reverse=True)
    assert amounts[0] == 5000.0


def test_get_top_transactions_fields(sample_transactions):
    result = get_top_transactions(sample_transactions, n=1)
    tx = result[0]
    assert set(tx.keys()) == {"date", "amount", "category", "description"}
    # Дата в формате dd.mm.yyyy
    assert tx["date"] == "16.06.2024"
    assert tx["category"] == "Электроника"
    assert tx["description"] == "DNS"


def test_get_top_transactions_invalid_date():
    tx = [{
        "Дата операции": "невалидная_дата",
        "Сумма операции": -100.0,
        "Категория": "Прочее",
        "Описание": "Test",
    }]
    result = get_top_transactions(tx, n=1)
    # Не должно упасть; дата останется как есть (первые 10 символов)
    assert result[0]["date"] == "невалидная"


# ---------- get_main_page_view ----------

def test_get_main_page_view_structure(sample_transactions):
    settings = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "TSLA"],
    }

    # Фиксируем «сейчас» на июнь 2024, чтобы данные попали в текущий месяц
    fixed_now = datetime(2024, 6, 20, 12, 0, 0)

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    with patch("src.views.datetime", FakeDateTime):
        result = get_main_page_view(sample_transactions, settings)

    assert set(result.keys()) == {
        "greeting",
        "cards",
        "top_transactions",
        "currency_rates",
        "stock_prices",
    }
    assert result["greeting"] in {
        "Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"
    }
    assert isinstance(result["cards"], list)
    assert len(result["top_transactions"]) == 5
    assert result["currency_rates"] == ["USD", "EUR"]
    assert result["stock_prices"] == ["AAPL", "TSLA"]


def test_get_main_page_view_filters_by_month(sample_transactions):
    """Транзакции прошлого месяца не должны попасть в отчёт."""
    old_tx = [{
        "Дата операции": "2020-01-01 12:00:00",
        "Сумма операции": -100000.0,
        "Категория": "Старое",
        "Описание": "Old",
        "Номер карты": "*0000",
        "Кешбэк": 0,
    }]
    settings = {"user_currencies": [], "user_stocks": []}
    fixed_now = datetime(2024, 6, 20, 12, 0, 0)

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    with patch("src.views.datetime", FakeDateTime):
        result = get_main_page_view(old_tx, settings)

    assert result["top_transactions"] == []
    assert result["cards"] == []
