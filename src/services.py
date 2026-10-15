import re
from collections import defaultdict
from datetime import datetime

# ---------- Сервис 1: Выгодные категории повышенного кешбэка ----------


def analyze_cashback_categories(
    data: list[dict], year: int, month: int
) -> dict[str, int]:
    """
    Анализирует, сколько кешбэка можно заработать на каждой категории
    за указанный месяц года.
    """
    result: dict[str, int] = defaultdict(int)
    for t in data:
        date_str = str(t.get("Дата операции", ""))
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if dt.year != year or dt.month != month:
            continue
        # Только расходы
        amount = float(t.get("Сумма операции", 0) or 0)
        if amount >= 0:
            continue
        category = str(t.get("Категория", "")) or "Без категории"
        cashback = float(t.get("Кешбэк", 0) or 0)
        result[category] += int(cashback)
    return dict(result)


# ---------- Сервис 2: Инвесткопилка ----------


def investment_bank(month: str, transactions: list[dict], limit: int) -> float:
    """
    Возвращает сумму, которую удалось бы отложить в Инвесткопилку.

    :param month: месяц в формате 'YYYY-MM'
    :param transactions: список транзакций
    :param limit: шаг округления (10, 50, 100)
    """
    total_saved = 0.0
    for t in transactions:
        date_str = str(t.get("Дата операции", ""))[:7]
        if date_str != month:
            continue
        amount = float(t.get("Сумма операции", 0) or 0)
        if amount >= 0:
            continue
        abs_amount = abs(amount)
        # Округляем вверх до ближайшего кратного limit
        rounded = ((abs_amount + limit - 1) // limit) * limit
        total_saved += rounded - abs_amount
    return round(total_saved, 2)


# ---------- Сервис 3: Простой поиск ----------


def simple_search(transactions: list[dict], query: str) -> list[dict]:
    """Возвращает транзакции, содержащие подстроку в описании или категории."""
    if not query:
        return []
    q = query.lower()
    result = []
    for t in transactions:
        desc = str(t.get("Описание", "")).lower()
        cat = str(t.get("Категория", "")).lower()
        if q in desc or q in cat:
            result.append(t)
    return result


# ---------- Сервис 4: Поиск по телефонным номерам ----------

PHONE_PATTERN = re.compile(
    r"(?:\+7|8)"  # +7 или 8
    r"[\s\-]?"  # разделитель
    r"\(?\d{3}\)?"  # код оператора (может быть в скобках)
    r"[\s\-]?"  # разделитель
    r"\d{2,3}"  # 2 или 3 цифры
    r"[\s\-]?"  # разделитель
    r"\d{2}"  # 2 цифры
    r"[\s\-]?"  # разделитель
    r"\d{2}"  # 2 цифры
)


def search_phone_numbers(transactions: list[dict]) -> list[dict]:
    """Возвращает транзакции, содержащие мобильные номера в описании."""
    return [
        tx for tx in transactions if PHONE_PATTERN.search(str(tx.get("Описание", "")))
    ]


# ---------- Сервис 5: Поиск переводов физлицам ----------

PERSON_PATTERN = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")


def search_person_transfers(transactions: list[dict]) -> list[dict]:
    """
    Возвращает транзакции, относящиеся к переводам физлицам:
    категория 'Переводы' и в описании имя + первая буква фамилии с точкой.
    """
    result = []
    for t in transactions:
        category = str(t.get("Категория", "")).strip()
        desc = str(t.get("Описание", "")).strip()
        if category == "Переводы" and PERSON_PATTERN.match(desc):
            result.append(t)
    return result
