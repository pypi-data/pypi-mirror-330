# HTML Generator

Библиотека для генерации HTML-страниц. Поддерживает добавление заголовков, CSS- и JS-файлов, а также секций контента.

## Установка

Установите библиотеку через pip:

```bash
pip install htmlgenim
```

## Использование
```bash
from htmlgenim.generator import HTML, Table

# Создаем экземпляр HTML
page = HTML()

# Устанавливаем заголовок
page.set_title("Моя страница")

# Добавляем CSS-файлы
page.css_link_add("styles.css")

# Добавляем JS-файлы
page.js_link_add("script.js")

# Добавляем секции контента с классами CSS
page.section_add("<h1>Привет, мир!</h1>", section_class="label")
page.section_add("<button>Это пример использования HTML генератора.</button>", section_class="button")

# Создаем таблицу
table = Table()
table.add_class("my-table")
table.add_row(['Ячейка 1', 'Ячейка 2'])
table.add_row(['Ячейка 3', 'Ячейка 4'])
page.table_add(table)

# Сохраняем HTML в файл
page.save_to_file("output.html")
```

## Upgrade
1. Возможность добавление таблицы
2. Можно указывать стили CSS к section