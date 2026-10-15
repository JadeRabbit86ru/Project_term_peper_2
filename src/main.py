import json

from src.services import (analyze_cashback_categories, investment_bank,
                          search_person_transfers, search_phone_numbers,
                          simple_search)
from src.utils import load_transactions_from_excel, load_user_settings
from src.views import get_main_page_view


def main():
    transactions = load_transactions_from_excel("data/operations.xlsx")
    settings = load_user_settings()

    # Главная страница
    main_view = get_main_page_view(transactions, settings)
    print(json.dumps(main_view, ensure_ascii=False, indent=2))

    # Пример: анализ кешбэка за декабрь 2021
    cashback = analyze_cashback_categories(transactions, 2021, 12)
    print("Кешбэк по категориям:", json.dumps(cashback, ensure_ascii=False, indent=2))

    # Пример: инвесткопилка за декабрь 2021 с шагом 50
    saved = investment_bank("2021-12", transactions, 50)
    print(f"Отложено в инвесткопилку: {saved} ₽")

    # Пример: поиск
    found = simple_search(transactions, "Магнит")
    print(f"Найдено транзакций: {len(found)}")

    # Поиск по телефонам
    phones = search_phone_numbers(transactions)
    print(f"Найдено транзакций с телефонами: {len(phones)}")

    # Поиск переводов физлицам
    transfers = search_person_transfers(transactions)
    print(f"Найдено переводов физлицам: {len(transfers)}")


if __name__ == "__main__":
    main()
