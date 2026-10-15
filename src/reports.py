from collections import defaultdict
from datetime import datetime
from typing import Any


def get_expenses_by_category(
    transactions: list[dict], year: int, month: int
) -> dict[str, Any]:
    """
    Отчёт по расходам за месяц с группировкой по категориям.
    Топ-7 категорий + «Остальное». Переводы и наличные выделены.
    """
    expenses: dict[str, float] = defaultdict(float)
    for t in transactions:
        date_str = str(t.get("Дата операции", ""))
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if dt.year != year or dt.month != month:
            continue
        amount = float(t.get("Сумма операции", 0) or 0)
        if amount >= 0:
            continue
        category = str(t.get("Категория", "")) or "Без категории"
        # Переводы и наличные выделяем в отдельные категории
        if category == "Переводы":
            key = "Переводы"
        elif category == "Наличные":
            key = "Наличные"
        else:
            key = category
        expenses[key] += abs(amount)

    # Сортируем по убыванию
    sorted_exp = sorted(expenses.items(), key=lambda x: x[1], reverse=True)

    # Выделяем топ-7 (исключая Переводы и Наличные, если они не в топе)
    special = {"Переводы", "Наличные"}
    main_categories = [(k, v) for k, v in sorted_exp if k not in special]
    other_sum = sum(v for k, v in sorted_exp if k not in special and k not in dict(main_categories[:7]))

    top7 = dict(main_categories[:7])
    other_sum += sum(
        v for k, v in sorted_exp
        if k not in special and k not in top7
    )
    if other_sum > 0:
        top7["Остальное"] = round(other_sum)

    # Добавляем переводы и наличные
    for k, v in sorted_exp:
        if k in special:
            top7[k] = round(v)

    # Округляем
    result = {k: round(v) for k, v in top7.items()}

    # Разбиваем на расходы и поступления
    income = sum(
        float(t.get("Сумма операции", 0) or 0)
        for t in transactions
        if _in_month(t, year, month) and float(t.get("Сумма операции", 0) or 0) > 0
    )
    total_expenses = sum(result.values())

    return {
        "expenses": result,
        "income": round(income),
        "total_expenses": total_expenses,
    }


def _in_month(t: dict, year: int, month: int) -> bool:
    date_str = str(t.get("Дата операции", ""))
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.year == year and dt.month == month
    except ValueError:
        return False
