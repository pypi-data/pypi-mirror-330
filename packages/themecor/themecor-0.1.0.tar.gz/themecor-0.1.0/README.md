# themecor

`themecor` is a Python package that provides a centralized theme manager to ensure visual consistency across different packages within an application. It offers styles and methods to display messages, prompts, and progress bars in a uniform manner.

## Installation

```bash
pip install themecor
```

**Note**: This package is under development and may contain breaking changes.

## Usage
Here's an example of how to use themecor:

```python
from themecor import ThemeManager

# Initialize the theme manager
theme_manager = ThemeManager()

# Use methods to display messages
theme_manager.info("Information message")
theme_manager.success("Success message")
theme_manager.warning("Warning message")
theme_manager.error("Error message")
theme_manager.debug("Debug message")

# Use methods to display headers and panels
theme_manager.header("Main Title", "Optional Subtitle")
theme_manager.panel("Panel content", "Panel Title")

# Use methods for prompts and tables
response = theme_manager.confirm("Confirm action?", default=True)
table = theme_manager.table(title="Data Table", headers=["Column 1", "Column 2"])
table.add_row("Data 1", "Data 2")
theme_manager.console.print(table)

# Use methods for progress bar management
progress, task_id = theme_manager.manage_progress(None, None, "Task in progress...", 100)
theme_manager.update_progress(progress, task_id, 50)
# ... (Your task code)
theme_manager.update_progress(progress, task_id, 100)
theme_manager.stop_progress(progress)
```


## Features
- **Centralized Theme Management**: Ensures a consistent look and feel throughout the application.
- **Customizable Styles**: Allows defining custom styles for messages, prompts, etc.
- **Rich Integration**: Uses the Rich library for colorful and styled displays.
- **Typer Integration**: Provides a pre-configured Typer instance for command-line management.
- **Progress Bar Management**: Simplifies the creation and management of progress bars.

## Configuration

You can customize the theme by passing a dictionary of custom styles when initializing ThemeManager:

```python
custom_theme = {
    "primary": "green",
    "success": "blue",
}

theme_manager = ThemeManager(custom_theme=custom_theme)
```

## Contribution

Contributions are welcome! Feel free to submit pull requests or report issues.

## License

This project is licensed under the MIT License.