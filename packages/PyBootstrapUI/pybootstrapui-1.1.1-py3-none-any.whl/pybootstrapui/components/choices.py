from pybootstrapui.utils.callbacks import wrap_callback
from . import add_handler
from .base import HTMLElement, HasValue
from typing import Callable, Awaitable, Union
import pybootstrapui.components.dynamics.queue as queue


class Option(HTMLElement):
    """
    A class representing an <option> element for a <select> dropdown.

    This class generates an HTML <option> element with the given label and value.

    Attributes:
        label (str): The label for the option.
        selected (bool): Whether the option is selected (default is False).
        value (str | None): The value of the option (default is None).
    """

    def __init__(
        self,
        label: str,
        selected: bool = False,
        value: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes an Option object with the specified label, selection status, and value.

        Args:
            label (str): The label for the option.
            selected (bool): Whether the option is selected (default is False).
            value (str | None): The value of the option (default is None).
            classes (list[str] | None): Optional list of classes to be applied to the <option> element.
            id (str | None): Optional unique ID for the <option> element.

        Example:
            option = Option(label="Option 1", value="1", selected=True)
        """
        super().__init__(classes, id)
        self.value = value
        self.label = label
        self.selected = selected

    def construct(self) -> str:
        """
        Generates the HTML code for the <option> element.

        Returns:
            str: The HTML code for the <option> element.

        Example:
            html = option.construct()
        """
        return f'<option class="{self.classes_str}" id="{self.id}" value="{self.value if self.value else self.label}" {"selected" if self.selected else ""}>{self.label}</option>'


class Choice(HasValue):
    """
    A class representing a <select> dropdown element containing multiple options.

    This class generates an HTML <select> element with a list of <option> elements.

    Attributes:
        options (list[Option]): A list of Option objects to be included in the <select> element.
        name (str | None): The name of the <select> element.
        on_choice (Callable | Awaitable | None): A callback to handle the onchange event.
    """

    def __init__(
        self,
        *options: Option,
        name: str | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
        on_choice: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
    ):
        """
        Initializes a Choice object with a list of options and an optional name for the <select> element.

        Args:
            *options (Option): A list of Option objects to be included in the <select> element.
            name (str | None): The name of the <select> element.
            classes (list[str] | None): Optional list of classes to be applied to the <select> element.
            id (str | None): Optional unique ID for the <select> element.
            on_choice (Callable | Awaitable | None): A callback function to handle the onchange event.

        Example:
            choice = Choice(
                options=[Option("Option 1", value="1"), Option("Option 2", value="2")],
                name="my-select",
                on_choice=my_callback
            )
        """
        super().__init__(classes, id)
        self.options = options
        self.name = name
        self.on_choice = on_choice

    def construct(self) -> str:
        """
        Generates the HTML code for the <select> dropdown element with options.

        Returns:
            str: The HTML code for the <select> element containing the options.

        Example:
            html = choice.construct()
        """

        # Register callback if provided
        if self.on_choice and self.id:
            add_handler("on_choice", self.id, wrap_callback(self.on_choice))

        compiled_child = "\n".join([child.construct() for child in self.options])
        return f"""<select {f'onchange="sendOnChoice(this.id)"' if self.on_choice else ''} class="form-select {self.classes_str}" id="{self.id}" name="{self.name}">{compiled_child}</select>"""
