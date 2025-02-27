import logging
from html import escape

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTML:
    def __init__(self):
        self.title = ""
        self.css_links = []
        self.js_links = []
        self.sections = []

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

    def section_add(self, content):
        """
        Добавляет секцию контента.
        """
        # Экранируем только текст внутри тегов, но не сами теги
        self.sections.append(content)  # Содержимое секции не экранируем, так как это HTML-код
        logger.info(f"Добавлена секция: {content}")

    def render(self):
        """
        Генерирует HTML-страницу на основе установленных данных.
        """
        html = ["<!DOCTYPE html>", "<html>", "<head>"]
        
        # Добавляем заголовок
        if self.title:
            html.append(f"<title>{self.title}</title>")
        
        # Добавляем CSS-файлы
        for css_link in self.css_links:
            html.append(f'<link rel="stylesheet" href="{css_link}">')
        
        # Добавляем JS-файлы
        for js_link in self.js_links:
            html.append(f'<script src="{js_link}"></script>')
        
        html.append("</head>")
        html.append("<body>")
        
        # Добавляем секции контента
        for section in self.sections:
            html.append(section)  # Секции добавляем как есть (HTML-код)
        
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