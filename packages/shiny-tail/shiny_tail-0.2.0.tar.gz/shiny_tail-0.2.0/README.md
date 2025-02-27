**shinytail**

A lightweight Python package for seamlessly integrating Tailwind CSS with Shiny for Python applications.

**Installation**

```
pip install shiny_tail
```

**Features**

- Add Tailwind CSS to Shiny with one line of code
- Support for Tailwind plugins and configurations
- Custom themes and styling
- No external CSS dependencies required
- Simple, intuitive API
- Responsive design out of the box

**Usage**

```python
from shiny import App, ui
from htmltools import tags
from shiny_tail import tailwind

# Configure Tailwind with plugins
tailwind.configure(
    plugins=["typography"],
    config={"theme": {"extend": {"colors": {"custom-blue": "#1e40af"}}}}
)

# Create a UI with Tailwind classes
app_ui = tailwind.page(
    tags.h1("Hello Tailwind", class_="text-3xl font-bold text-custom-blue")
)

def server(input, output, session):
    pass

app = App(app_ui, server)
```

**Requirements**

- Python >=3.7
- shiny >=0.5.0
- htmltools >=0.4.0

**License**
MIT

**Contributing**

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

**Support**
For issues and feature requests, please use the **issue tracker**.
