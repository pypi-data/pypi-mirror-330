# HTML Generator

Library for generating HTML pages. Supports adding headers, CSS and JS files, and content tags.

## Installation

Install the library via pip:

```bash
pip install htmlgenim
```

## Usage
```bash
from htmlgenim.generator import HTML, Table

# Creating an HTML Instance
page = HTML()

# Setting the title
page.set_title("My page")

# Adding CSS files
page.css_link_add("styles.css")
# page.css_link_add("https://example.com/styles.css")

# Adding JS files
page.js_link_add("script.js")
# page.js_link_add("https://example.com/script.js")

# Adding elements with attributes
page.add_element("h1", "Hello World!", class_="header", id="main-header")
page.add_element("p", "This is an example of using an HTML generator.", class_="content")
page.add_element("a", "Link to Example", href="https://example.com", class_="link")
page.add_element("input", type="radio", name="season", id="spring", value="Spring")
page.add_element("img", src="image.jpg", alt="Description of the image", class_="image")

# Create a table
table = Table()
table.add_class("my-table")
table.add_attr("border", "1")
table.add_row(["Cell 1", "Cell 2"])
table.add_row(["Cell 3", "Cell 4"])
page.table_add(table)

# Saving HTML to a file
page.save_to_file("output.html")
```

## Upgrade
1. Ability to add a table.
2. You can specify CSS styles and other attributes to tags.
3. A log file is created that displays page generation information.