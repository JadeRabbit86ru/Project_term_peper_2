import pytest
from src.services import (
    analyze_cashback_categories,
    investment_bank,
    simple_search,
    search_phone_numbers,
    search_person_transfers,
)


@pytest.fixture
def sample_transactions():
    return [
        {
            "Дата операции": "2021-12-15 12:00:00",
            "Сумма операции": -1000.0,
            "Категория": "Супермаркеты",
            "Описание": "Магнит",
            "Кешбэк": 10.0,
        },
        {
            "Дата операции": "2021-12-20 15:00:00",
            "Сумма операции": -500.0,
            "Категория": "Фастфуд",
            "Описание": "McDonald's",
            "Кешбэк": 5.0,
        },
        {
            "Дата операции": "2021-12-25 10:00:00",
            "Сумма операции": -1712.0,
            "Категория": "Супермаркеты",
            "Описание": "Перекрёсток",
            "Кешбэк": 17.0,
        },
    ]


def test_analyze_cashback_categories(sample_transactions):
    result = analyze_cashback_categories(sample_transactions, 2021, 12)
    assert result["Супермаркеты"] == 27
    assert result["Фастфуд"] == 5


def test_investment_bank(sample_transactions):
    result = investment_bank("2021-12", sample_transactions, 50)
    # 1000 -> 1000 (0), 500 -> 500 (0), 1712 -> 1750 (38)
    assert result == 38.0


def test_simple_search(sample_transactions):
    result = simple_search(sample_transactions, "магнит")
    assert len(result) == 1
    assert result[0]["Описание"] == "Магнит"


def test_search_phone_numbers():
    tx = [
        {"Описание": "Я МТС +7 921 11-22-33", "Категория": "Связь"},
        {"Описание": "Тинькофф Мобайл +7 995 555-55-55", "Категория": "Связь"},
        {"Описание": "Просто покупка", "Категория": "Супермаркеты"},
    ]
    result = search_phone_numbers(tx)
    assert len(result) == 2


def test_search_person_transfers():
    tx = [
        {"Описание": "Валерий А.", "Категория": "Переводы"},
        {"Описание": "Сергей З.", "Категория": "Переводы"},
        {"Описание": "Магнит", "Категория": "Супермаркеты"},
        {"Описание": "Перевод Кредитная карта", "Категория": "Переводы"},
    ]
    result = search_person_transfers(tx)
    assert len(result) == 2
