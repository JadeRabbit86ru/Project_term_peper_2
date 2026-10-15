from collections import defaultdict
from datetime import datetime
from typing import Any


def _in_month(t: dict, year: int, month: int) -> bool:
    date_str = str(t.get("Дата операции", ""))
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.year == year and dt.month == month
    except ValueError:
        return False


def get_expenses_by_category(
    transactions: list[dict], year: int, month: int
) -> dict[str, Any]:
    """
    Отчёт по расходам за месяц с группировкой по категориям.
    Топ-7 категорий + «Остальное». Переводы и наличные выделены.
    """
    expenses: dict[str, float] = defaultdict(float)

    for t in transactions:
        if not _in_month(t, year, month):
            continue
        amount = float(t.get("Сумма операции", 0) or 0)
        if amount >= 0:
            continue
        category = str(t.get("Категория", "")) or "Без категории"
        expenses[category] += abs(amount)

    # Сортируем все категории по убыванию суммы
    sorted_exp = sorted(expenses.items(), key=lambda x: x[1], reverse=True)

    # Переводы и Наличные идут отдельными строками,
    # не участвуют в формировании топ-7 и «Остального»
    special = {"Переводы", "Наличные"}
    special_items = [(k, v) for k, v in sorted_exp if k in special]
    regular_items = [(k, v) for k, v in sorted_exp if k not in special]

    # Топ-7 из «обычных» категорий
    top7 = dict(regular_items[:7])

    # Всё, что не вошло в топ-7, — в «Остальное» (СЧИТАЕМ ОДИН РАЗ!)
    other_sum = sum(v for _, v in regular_items[7:])
    if other_sum > 0:
        top7["Остальное"] = round(other_sum)

    # Добавляем Переводы и Наличные отдельно
    for k, v in special_items:
        top7[k] = round(v)

    # Округляем значения
    result = {k: round(v) for k, v in top7.items()}

    # Доход за месяц
    income = sum(
        float(t.get("Сумма операции", 0) or 0)
        for t in transactions
        if _in_month(t, year, month) and float(t.get("Сумма операции", 0) or 0) > 0
    )

    return {
        "expenses": result,
        "income": round(income),
        "total_expenses": sum(result.values()),
    }
