import pytest

from src.reports import get_expenses_by_category


@pytest.fixture
def sample_transactions():
    """Транзакции за декабрь 2021 с разными категориями."""
    base = {"Дата операции": "2021-12-15 12:00:00"}
    return [
        {**base, "Сумма операции": -1000.0, "Категория": "Супермаркеты"},
        {**base, "Сумма операции": -800.0,  "Категория": "Фастфуд"},
        {**base, "Сумма операции": -600.0,  "Категория": "Транспорт"},
        {**base, "Сумма операции": -500.0,  "Категория": "Аптеки"},
        {**base, "Сумма операции": -400.0,  "Категория": "Дом и ремонт"},
        {**base, "Сумма операции": -300.0,  "Категория": "Одежда"},
        {**base, "Сумма операции": -200.0,  "Категория": "Связь"},
        {**base, "Сумма операции": -100.0,  "Категория": "Книги"},
        {**base, "Сумма операции": -50.0,   "Категория": "Цветы"},
        {**base, "Сумма операции": -2000.0, "Категория": "Переводы"},
        {**base, "Сумма операции": -500.0,  "Категория": "Наличные"},
        {**base, "Сумма операции": 5000.0,  "Категория": "Пополнения"},   # поступление
        {"Дата операции": "2021-11-15 12:00:00",
         "Сумма операции": -9999.0, "Категория": "Не в этом месяце"},
    ]


def test_get_expenses_by_category_basic(sample_transactions):
    result = get_expenses_by_category(sample_transactions, 2021, 12)
    assert "expenses" in result
    assert "income" in result
    assert "total_expenses" in result


def test_top7_and_other(sample_transactions):
    result = get_expenses_by_category(sample_transactions, 2021, 12)
    expenses = result["expenses"]

    # Топ-7 категорий по убыванию
    assert expenses["Супермаркеты"] == 1000
    assert expenses["Фастфуд"] == 800
    assert expenses["Транспорт"] == 600
    assert expenses["Аптеки"] == 500
    assert expenses["Дом и ремонт"] == 400
    assert expenses["Одежда"] == 300
    assert expenses["Связь"] == 200

    # Книги (100) и Цветы (50) ушли в «Остальное»
    assert expenses["Остальное"] == 150


def test_transfers_and_cash_are_separated(sample_transactions):
    result = get_expenses_by_category(sample_transactions, 2021, 12)
    expenses = result["expenses"]

    assert expenses["Переводы"] == 2000
    assert expenses["Наличные"] == 500


def test_income_calculated(sample_transactions):
    result = get_expenses_by_category(sample_transactions, 2021, 12)
    assert result["income"] == 5000


def test_other_month_excluded(sample_transactions):
    """Транзакция за ноябрь не должна попасть в декабрьский отчёт."""
    result = get_expenses_by_category(sample_transactions, 2021, 12)
    assert "Не в этом месяце" not in result["expenses"]


def test_total_expenses_sum(sample_transactions):
    result = get_expenses_by_category(sample_transactions, 2021, 12)
    expected_total = sum(result["expenses"].values())
    assert result["total_expenses"] == expected_total


def test_empty_transactions():
    result = get_expenses_by_category([], 2021, 12)
    assert result["expenses"] == {}
    assert result["income"] == 0
    assert result["total_expenses"] == 0
