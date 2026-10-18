# Анализ транзакций

Приложение для анализа банковских транзакций из Excel-файла. Генерирует JSON-данные для веб-страниц, формирует отчёты и предоставляет сервисы анализа: кешбэк по категориям, «Инвесткопилка», поиск по описанию, поиск телефонных номеров и переводов физлицам.

---

## 📋 Оглавление

- [Возможности](#-возможности)
- [Структура проекта](#-структура-проекта)
- [Требования](#-требования)
- [Установка](#-установка)
- [Настройка](#-настройка)
- [Запуск](#-запуск)
- [Тестирование](#-тестирование)
- [Линтеры и типизация](#-линтеры-и-типизация)
- [Примеры использования](#-примеры-использования)
- [Автор](#-автор)
- [Лицензия](#-лицензия)

---

## 🚀 Возможности

### Главная страница (`views.py`)

Формирует JSON для веб-интерфейса:

- **Приветствие** по времени суток:
  - 06:00–11:59 — «Доброе утро»
  - 12:00–17:59 — «Добрый день»
  - 18:00–22:59 — «Добрый вечер»
  - 23:00–05:59 — «Доброй ночи»
- **Информация о картах**: последние 4 цифры, сумма расходов, накопленный кешбэк.
- **Топ-5 транзакций** за текущий месяц по убыванию суммы (поля: `date`, `amount`, `category`, `description`).
- **Курсы валют** из настроек пользователя (`user_settings.json`).
- **Цены акций** из настроек пользователя.

### Сервисы (`services.py`)

| Сервис | Функция | Описание |
|---|---|---|
| **Выгодные категории кешбэка** | `analyze_cashback_categories` | Сколько кешбэка можно заработать на каждой категории за указанный месяц |
| **Инвесткопилка** | `investment_bank` | Сумма, которую удалось бы отложить через округление трат (шаг 10/50/100 ₽) |
| **Простой поиск** | `simple_search` | Поиск по подстроке в описании и категории (регистронезависимый) |
| **Поиск телефонов** | `search_phone_numbers` | Находит транзакции с мобильными номерами в описании |
| **Поиск переводов физлицам** | `search_person_transfers` | Находит транзакции категории «Переводы» с именем и инициалом фамилии |

### Отчёты (`reports.py`)

- Расходы по категориям за месяц.
- Топ-7 категорий + «Остальное».
- Переводы и наличные выделены отдельно.
- Сумма поступлений за период.

---

## 📁 Структура проекта

```
Project_term_peper_2/
├── src/
│   ├── __init__.py
│   ├── main.py          # точка входа
│   ├── utils.py         # чтение Excel, приветствие, карты
│   ├── views.py         # главная страница (JSON)
│   ├── services.py      # бизнес-сервисы
│   └── reports.py       # отчёты
├── data/
│   └── operations.xlsx  # исходные транзакции
├── test/
│   ├── __init__.py
│   ├── test_utils.py
│   ├── test_views.py
│   ├── test_services.py
│   └── test_reports.py
├── user_settings.json   # настройки пользователя
├── .env                 # секреты (не коммитится)
├── .env_template        # шаблон для .env
├── .flake8              # конфиг flake8
├── mypy.ini             # конфиг mypy
├── pyproject.toml       # зависимости и настройки poetry
├── .gitignore
└── README.md
```

---

## ⚙️ Требования

- **Python 3.11+** (используются синтаксис `list[dict]`, `X | None`).
- **pip** или **poetry** для управления зависимостями.
- **Git** для клонирования репозитория.

---

## 📦 Установка

### 1. Клонирование репозитория

```bash
git clone <название репозитория>
cd Project_term_peper_2
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv
```

Активация:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (cmd):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Установка зависимостей

**Через poetry (рекомендуется):**

```bash
pip install poetry
poetry install
```

**Через pip:**

```bash
pip install pandas openpyxl python-dotenv requests
pip install pytest flake8 mypy
```

---

## 🔧 Настройка

### Файл `.env`

Скопируйте шаблон и заполните своими значениями:

```bash
cp .env_template .env
```

**`.env`:**
```ini
# API-токены для внешних сервисов
EXCHANGE_API_KEY=your_exchange_api_key_here
STOCK_API_KEY=your_stock_api_key_here

# Пути к файлам
OPERATIONS_FILE_PATH=data/operations.xlsx
USER_SETTINGS_PATH=user_settings.json

# Уровень логирования
LOG_LEVEL=INFO
```

⚠️ **Файл `.env` не коммитится в репозиторий** — он добавлен в `.gitignore`.

### Файл `user_settings.json`

Список валют и акций для отслеживания:

```json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```

---

## ▶️ Запуск

```bash
python -m src.main
```

Или напрямую:

```bash
python src/main.py
```

На выходе — JSON для главной страницы и результаты работы сервисов в консоли.

---

## 🧪 Тестирование

### Запуск всех тестов

```bash
pytest test/ -v
```

### Запуск конкретного файла

```bash
pytest test/test_services.py -v
```

### Запуск конкретного теста

```bash
pytest test/test_services.py::test_search_phone_numbers -v
```

### Покрытие кода

```bash
pytest test/ --cov=src --cov-report=term-missing
```

---

## 🧹 Линтеры и типизация

### flake8 (стиль кода)

```bash
flake8 src/ test/
```

Конфигурация — `.flake8`:
- `max-line-length = 100`
- Игнорируются `E203`, `W503` (конфликты с black)
- Для `__init__.py` разрешены `F401`, `F403`

### mypy (статическая типизация)

```bash
mypy src/
```

Конфигурация — `mypy.ini`:
- `disallow_untyped_defs = True` — все функции с аннотациями
- `strict_optional = True` — строгий контроль `None`
- `warn_return_any = True` — предупреждения о возврате `Any`

### Проверка всего сразу

```bash
flake8 src/ test/ && mypy src/ && pytest test/ -v
```

---

## 💡 Примеры использования

### 1. Анализ выгодных категорий кешбэка

```python
from src.services import analyze_cashback_categories

transactions = [...]  # список словарей
result = analyze_cashback_categories(transactions, year=2021, month=12)
print(result)
# {"Супермаркеты": 27, "Фастфуд": 5, ...}
```

### 2. Инвесткопилка

```python
from src.services import investment_bank

saved = investment_bank("2021-12", transactions, limit=50)
print(f"Отложено: {saved} ₽")
# Отложено: 38.0 ₽
```

### 3. Поиск по описанию

```python
from src.services import simple_search

found = simple_search(transactions, "магнит")
print(f"Найдено: {len(found)}")
```

### 4. Поиск телефонных номеров

```python
from src.services import search_phone_numbers

phones = search_phone_numbers(transactions)
print(f"Транзакций с телефонами: {len(phones)}")
```

### 5. Поиск переводов физлицам

```python
from src.services import search_person_transfers

transfers = search_person_transfers(transactions)
# Находит: "Валерий А.", "Сергей З.", "Артем П."
```

### 6. Отчёт по расходам

```python
from src.reports import get_expenses_by_category

report = get_expenses_by_category(transactions, year=2021, month=12)
print(report["expenses"])
# {"Супермаркеты": 1000, "Фастфуд": 800, ..., "Остальное": 150}
```

---

## 👤 Автор

**Манаенков Илья Владимирович**

- 📧 Email: [alastor86@yandex.ru](mailto:alastor86@yandex.ru)
- 📧 Доп. Email: [jade_rabbit_86ru@hotmail.com](mailto:jade_rabbit_86ru@hotmail.com)
- 🐙 GitHub: [JadeRabbit86ru](https://github.com/JadeRabbit86ru)

---

## 📄 Лицензия

Проект создан в учебных целях в рамках курсовой работы. Свободен для использования и модификации.

---

## 🙏 Благодарности

- **SkyPro** — за постановку задачи и материалы курса.
- Сообществу Python — за отличные библиотеки: `pandas`, `openpyxl`, `requests`, `pytest`, `mypy`, `flake8`.
