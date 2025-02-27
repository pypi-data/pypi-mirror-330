# HTML Generator

Библиотека для генерации HTML-страниц. Поддерживает добавление заголовков, CSS- и JS-файлов, а также секций контента.

## Установка

Установите библиотеку через pip:

```bash
pip install htmlgenim
```

## Использование
```bash
from htmlgenim.generator import HTML

# Создаем экземпляр HTML
page = HTML()

# Устанавливаем заголовок
page.set_title("Моя страница")

# Добавляем CSS-файлы
page.css_link_add("styles.css")

# Добавляем JS-файлы
page.js_link_add("script.js")

# Добавляем секции контента
page.section_add("<h1>Привет, мир!</h1>")
page.section_add("<p>Это пример использования HTML генератора.</p>")

# Сохраняем HTML в файл
page.save_to_file("output.html")
```