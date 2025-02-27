from htmltools import tags
from shiny import App

from shiny_tail import tailwind

# Configure Tailwind with plugins
tailwind.configure(
    plugins=["typography"],
    config={"theme": {"extend": {"colors": {"custom-blue": "#1e40af"}}}},
)

# Create a UI with Tailwind classes
app_ui = tailwind.page(
    tags.h1("Hello Tailwind", class_="text-3xl font-bold text-custom-blue")
)


def server(input, output, session):
    pass


app = App(app_ui, server)
