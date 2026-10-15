from datetime import datetime
from typing import Any

from src.utils import get_card_info, get_greeting


def get_top_transactions(transactions: list[dict], n: int = 5) -> list[dict]:
    """Топ-N транзакций по убыванию суммы (по модулю)."""
    sorted_tx = sorted(
        transactions,
        key=lambda item: abs(float(tx.get("Сумма операции", 0) or 0)),
        reverse=True,
    )[:n]
    result = []
    for tx in sorted_tx:
        date_str = str(tx.get("Дата операции", ""))[:10]
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = dt.strftime("%d.%m.%Y")
        except ValueError:
            formatted_date = date_str
        result.append({
            "date": formatted_date,
            "amount": float(tx.get("Сумма операции", 0) or 0),
            "category": str(tx.get("Категория", "")),
            "description": str(tx.get("Описание", "")),
        })
    return result


def get_main_page_view(transactions: list[dict],) -> dict[str, Any]:
    """
    Формирует JSON для главной страницы:
    приветствие, карты, топ-5 транзакций, курсы валют, цены акций.
    """
    now = datetime.now()
    start = now.replace(day=1)
    end = now

    # Фильтруем транзакции за текущий месяц
    month_tx = [
        t for t in transactions
        if start <= datetime.strptime(str(t.get("Дата операции", ""))[:10], "%Y-%m-%d") <= end
    ]

    return {
        "greeting": get_greeting(),
        "cards": get_card_info(month_tx),
        "top_transactions": get_top_transactions(month_tx, 5),
        "currency_rates": [],  # заполняется через API
        "stock_prices": [],    # заполняется через API
    }
