# SauceDemo Automated Tests

Цей репозиторій містить набір автоматизованих тестів для сайту [saucedemo.com](https://www.saucedemo.com/) за допомогою Python, pytest та Selenium.


## Що тестується
- **Успішний вхід в систему** (`test_successful_login`)
- **Неуспішний вхід** (`test_unsuccessful_login`)
- **Редірект після логіну** на сторінку з товарами (`test_redirect_after_login`)
- **Додавання товару в корзину** та зміна кнопки з `Add to Cart` на `Remove` (`test_add_to_cart_button_changes`)
- **Перевірка, що товар зʼявився в корзині** після додавання (`test_product_appears_in_cart`)

## Початок роботи

Як пакетний менеджер використовується **uv** від **astral.sh**.
Інструкція зі встановлення і налаштування: https://docs.astral.sh/uv/getting-started/installation/
### 1. Створення віртуального оточення

```bash
uv venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate
````

### 2. Встановлення залежностей

Замість `pip`, використовуйте **uv** для встановлення залежностей із `pyproject.toml`:

```bash
uv sync
```

### 3. Запуск лінтингу та форматування коду

* **Ruff** для перевірки стилю:

  ```bash
  uv run ruff check --fix.
  ```

### 4. Запуск тестів

```bash
uv run pytest tests/
```

> Використання `uv run pytest tests/` гарантує коректний запуск у вашому середовищі.

### 5. Додаткові плагіни

Для генерації HTML-звіту по тестах можна додати плагін **pytest-html**:

```bash
uv add pytest-html
uv run pytest tests/ --html=report.html
```
