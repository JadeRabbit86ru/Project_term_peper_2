import json
from datetime import datetime
from typing import Any

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def load_transactions_from_excel(path: str) -> list[dict[str, Any]]:
    """Читает Excel-файл и возвращает список транзакций."""
    df = pd.read_excel(path)
    # Приводим даты к строкам формата YYYY-MM-DD HH:MM:SS
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], dayfirst=True
    ).dt.strftime("%Y-%m-%d %H:%M:%S")
    df["Дата платежа"] = pd.to_datetime(
        df["Дата платежа"], dayfirst=True, errors="coerce"
    ).dt.strftime("%Y-%m-%d")
    # Заменяем NaN на пустые строки
    df = df.where(pd.notnull(df), "")
    return df.to_dict(orient="records")


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_info(transactions: list[dict]) -> list[dict]:
    """Возвращает информацию о картах: номер, общая сумма расходов, кешбэк."""
    cards: dict[str, dict] = {}
    for t in transactions:
        card = str(t.get("Номер карты", "")).strip()
        if not card or card.lower() == "nan":
            continue
        # Маска вида *1234
        if card not in cards:
            cards[card] = {"last_digits": card[-4:], "total_spent": 0.0, "cashback": 0.0}
        amount = float(t.get("Сумма операции", 0) or 0)
        cashback = float(t.get("Кешбэк", 0) or 0)
        if amount < 0:
            cards[card]["total_spent"] += abs(amount)
            cards[card]["cashback"] += cashback
    result = []
    for card, data in cards.items():
        result.append({
            "last_digits": data["last_digits"],
            "total_spent": round(data["total_spent"], 2),
            "cashback": round(data["cashback"], 2),
        })
    return result


def load_user_settings(path: str = "user_settings.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_by_date_range(
    transactions: list[dict], start: str, end: str
) -> list[dict]:
    """Фильтрует транзакции по диапазону дат (YYYY-MM-DD)."""
    result = []
    for t in transactions:
        date_str = str(t.get("Дата операции", ""))[:10]
        if start <= date_str <= end:
            result.append(t)
    return result
