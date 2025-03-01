import logging
from html import escape

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("html_generator.log")
    ]
)
logger = logging.getLogger(__name__)

class HTML:
    def __init__(self):
        self.title = ""
        self.css_links = []
        self.js_links = []
        self.content = []  # Список для хранения контента
        self.meta_tags = []
        self.inline_css = ""
        self.inline_js = ""
        self.tables = []

    def set_title(self, title):
        """
        Устанавливает заголовок страницы.
        """
        self.title = escape(title)  # Экранируем только текст заголовка
        logger.info(f"Заголовок установлен: {self.title}")

    def css_link_add(self, url):
        """
        Добавляет ссылку на CSS-файл.
        """
        self.css_links.append(url)  # URL не экранируем, так как это безопасные данные
        logger.info(f"Добавлен CSS-файл: {url}")

    def js_link_add(self, url):
        """
        Добавляет ссылку на JS-файл.
        """
        self.js_links.append(url)  # URL не экранируем, так как это безопасные данные
        logger.info(f"Добавлен JS-файл: {url}")

    def add_element(self, tag, content="", **attrs):
        """
        Добавляет HTML-элемент с указанными атрибутами и содержимым.
        :param tag: Имя тега (например, "h1", "input", "a").
        :param content: Содержимое элемента (для тегов, которые его поддерживают).
        :param attrs: Атрибуты элемента (например, class="my-class", id="my-id").
        """
        # Собираем атрибуты в строку
        attrs_str = " ".join([f'{key}="{escape(str(value))}"' for key, value in attrs.items()])
        
        # Формируем HTML-элемент
        if content:
            element = f"<{tag} {attrs_str}>{escape(content)}</{tag}>"
        else:
            element = f"<{tag} {attrs_str} />"
        
        self.content.append(element)
        logger.info(f"Добавлен элемент: {element}")

    def add_meta_tag(self, name, content):
        """
        Добавляет метатег.
        """
        self.meta_tags.append(f'<meta name="{name}" content="{escape(content)}">')
        logger.info(f"Добавлен метатег: {name}={content}")

    def add_inline_css(self, css):
        """
        Добавляет inline CSS.
        """
        self.inline_css = f"<style>{css}</style>"
        logger.info("Добавлен inline CSS")

    def add_inline_js(self, js):
        """
        Добавляет inline JS.
        """
        self.inline_js = f"<script>{js}</script>"
        logger.info("Добавлен inline JS")

    def table_add(self, table):
        """
        Добавляет таблицу на страницу.
        """
        self.content.append(table.render())
        logger.info("Добавлена таблица на страницу")

    def render(self):
        """
        Генерирует HTML-страницу на основе установленных данных.
        """
        html = ["<!DOCTYPE html>", "<html>", "<head>"]
        
        # Добавляем метатеги
        for meta_tag in self.meta_tags:
            html.append(meta_tag)
        
        # Добавляем заголовок
        if self.title:
            html.append(f"<title>{self.title}</title>")
        
        # Добавляем CSS-файлы
        for css_link in self.css_links:
            html.append(f'<link rel="stylesheet" href="{css_link}">')
        
        # Добавляем inline CSS
        if self.inline_css:
            html.append(self.inline_css)
        
        # Добавляем JS-файлы
        for js_link in self.js_links:
            html.append(f'<script src="{js_link}"></script>')
        
        # Добавляем inline JS
        if self.inline_js:
            html.append(self.inline_js)
        
        html.append("</head>")
        html.append("<body>")
        
        # Добавляем контент
        for element in self.content:
            html.append(element)
        
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)

    def save_to_file(self, output_file):
        """
        Сохраняет сгенерированный HTML в файл.
        """
        html_content = self.render()
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)
        logger.info(f"HTML-файл сохранен: {output_file}")


class Table:
    def __init__(self):
        self.rows = []
        self.classes = []
        self.attrs = {}

    def add_class(self, class_name):
        """
        Добавляет класс CSS к таблице.
        """
        self.classes.append(class_name)
        logger.info(f"Добавлен класс таблицы: {class_name}")

    def add_attr(self, attr_name, attr_value):
        """
        Добавляет атрибут к таблице.
        """
        self.attrs[attr_name] = attr_value
        logger.info(f"Добавлен атрибут таблицы: {attr_name}={attr_value}")

    def add_row(self, cells):
        """
        Добавляет строку в таблицу.
        """
        self.rows.append(cells)
        logger.info(f"Добавлена строка: {cells}")

    def render(self):
        """
        Генерирует HTML-код таблицы.
        """
        # Собираем атрибуты таблицы
        attrs = self.attrs.copy()
        if self.classes:
            attrs["class"] = " ".join(self.classes)
        
        attrs_str = " ".join([f'{key}="{escape(str(value))}"' for key, value in attrs.items()])
        
        table_html = [f"<table {attrs_str}>"]
        
        for row in self.rows:
            table_html.append("<tr>")
            for cell in row:
                table_html.append(f"<td>{escape(cell)}</td>")
            table_html.append("</tr>")
        
        table_html.append("</table>")
        return "".join(table_html)