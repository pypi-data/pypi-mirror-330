import json
import os
from typing import Dict, List, Optional, Union
from shiny import App, ui
from htmltools import HTMLDependency, tags

class ShinyTailwind:
    """
    A package to easily integrate Tailwind CSS with Shiny for Python applications.
    """

    def __init__(self, version: str = "3.3.1"):
        """
        Initialize the ShinyTailwind package.

        Args:
            version: The Tailwind CSS version to use.
        """
        self.version = version
        self._default_plugins = []
        self._default_config = {}
        self._default_styles = ""

    def configure(self, 
                plugins: Optional[List[str]] = None, 
                config: Optional[Dict] = None, 
                styles: Optional[str] = None) -> None:
        """
        Set default configuration for Tailwind CSS.

        Args:
            plugins: List of Tailwind plugins to use.
            config: Tailwind configuration as a dictionary.
            styles: Custom Tailwind CSS styles.
        """
        if plugins:
            self._default_plugins = plugins
        if config:
            self._default_config = config
        if styles:
            self._default_styles = styles

    def dependency(self, 
                  plugins: Optional[List[str]] = None, 
                  config: Optional[Dict] = None, 
                  styles: Optional[str] = None) -> HTMLDependency:
        """
        Create an HTMLDependency for Tailwind CSS.

        Args:
            plugins: List of Tailwind plugins to use.
            config: Tailwind configuration as a dictionary.
            styles: Custom Tailwind CSS styles.

        Returns:
            An HTMLDependency object for Tailwind CSS.
        """
        # Use provided values or fall back to defaults
        plugins = plugins or self._default_plugins
        config = config or self._default_config
        styles = styles or self._default_styles

        # Construct the CDN URL
        href = "https://cdn.tailwindcss.com"
        if plugins and len(plugins) > 0:
            href += f"?plugins={','.join(plugins)}"

        # Create the head elements
        head = [tags.script(src=href)]
        
        # Add the Tailwind configuration if provided
        if config:
            head.append(tags.script(f"tailwind.config = {json.dumps(config)}"))
        
        # Add custom styles if provided
        if styles:
            head.append(tags.style(styles, type="text/tailwindcss"))
        
        # Return the HTML dependency
        return HTMLDependency(
            name="tailwind",
            version=self.version,
            head=head
        )

    def page(self, 
             *args, 
             plugins: Optional[List[str]] = None, 
             config: Optional[Dict] = None, 
             styles: Optional[str] = None, 
             **kwargs) -> ui.TagList:
        """
        Create a Shiny page with Tailwind CSS included.

        Args:
            *args: Arguments to pass to ui.page_fluid.
            plugins: List of Tailwind plugins to use.
            config: Tailwind configuration as a dictionary.
            styles: Custom Tailwind CSS styles.
            **kwargs: Keyword arguments to pass to ui.page_fluid.

        Returns:
            A ui.TagList object with Tailwind CSS added.
        """
        # Get the Tailwind dependency
        tailwind_dep = self.dependency(plugins, config, styles)
        
        # Create the page with the dependency and elements
        return ui.page_fluid(
            tailwind_dep,
            *args,
            **kwargs
        )

    def apply_classes(self, element, classes: str) -> ui.Tag:
        """
        Apply Tailwind classes to an HTML element.

        Args:
            element: An HTML element created with htmltools.tags.
            classes: A string of Tailwind CSS classes.

        Returns:
            The HTML element with the Tailwind classes applied.
        """
        # Split classes and remove any empty ones
        class_list = [c for c in classes.split() if c]
        
        # Get existing classes from the element
        existing_classes = getattr(element, "class_", "").split()
        
        # Combine classes and apply them to the element
        all_classes = " ".join(existing_classes + class_list)
        element.attrs["class"] = all_classes
        
        return element

# Create a global instance
tailwind = ShinyTailwind()

# Example of a predefined theme function
def tailwind_theme(primary_color: str = "#3b82f6",  # blue-500
                  secondary_color: str = "#6b7280",  # gray-500
                  success_color: str = "#10b981",  # emerald-500
                  danger_color: str = "#ef4444",  # red-500
                  warning_color: str = "#f59e0b",  # amber-500
                  info_color: str = "#3b82f6",  # blue-500
                  ) -> Dict:
    """
    Create a Tailwind theme configuration with custom colors.

    Args:
        primary_color: The primary color for the application.
        secondary_color: The secondary color for the application.
        success_color: The color for success messages.
        danger_color: The color for error messages.
        warning_color: The color for warning messages.
        info_color: The color for information messages.

    Returns:
        A Tailwind configuration dictionary.
    """
    return {
        "theme": {
            "extend": {
                "colors": {
                    "primary": primary_color,
                    "secondary": secondary_color,
                    "success": success_color,
                    "danger": danger_color,
                    "warning": warning_color,
                    "info": info_color,
                }
            }
        }
    }