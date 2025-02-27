# markdown-dom

🌳 An elegant Python library for handling Markdown with a DOM-like structure

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)

## 🌟 Features

- 🎯 Handle Markdown with a hierarchical DOM-like structure
- 🔄 Dynamic Markdown generation and management
- 🧩 Modular structure for high reusability
- 🎨 Intuitive and easy-to-use API

## 🚀 Installation

```bash
pip install markdown-dom
```

## 📖 Usage

```python
from markdown_dom import MarkdownSection, MarkdownSectionTitle

# Create hierarchical structure
doc = MarkdownSection(
    MarkdownSectionTitle("Project Title"),
    MarkdownSection(
        MarkdownSectionTitle("Subsection"),
        "This is a description.",
        MarkdownSection(
            MarkdownSectionTitle("Nested Section"),
            "Description at a deeper level"
        )
    )
)

# Render as Markdown
print(doc.render())
```

Output:
```markdown
# Project Title
## Subsection
This is a description.
### Nested Section
Description at a deeper level
```

## 🛠️ Requirements

- Python 3.10 or higher
- pydantic >= 2.10.3

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and pull requests.

## 📜 License

Released under the MIT License. See [LICENSE](LICENSE) for details.


