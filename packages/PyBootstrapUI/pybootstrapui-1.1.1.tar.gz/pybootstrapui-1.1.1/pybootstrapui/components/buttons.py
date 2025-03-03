from typing import Callable, Awaitable, Union
from pybootstrapui.components.dynamics.client_to_server import add_handler
from pybootstrapui.utils.callbacks import wrap_callback
from pybootstrapui.components.text import BootstrapIcon
from .base import HTMLElement
from pybootstrapui.modifiers.buttons import ButtonModifier
from .dynamics import queue


class Button(HTMLElement):
    """
    A class representing an HTML <button> element.

    Attributes:
        label (str | None): The text label of the button.
        style_type (str): The style type of the button (default is 'primary').
        type (str | None): The type of the button (e.g., 'submit', 'button').
        callback (Callable | Awaitable | None): A server-side function to handle button clicks.
        data (str): Additional data associated with the button.
        icon (BootstrapIcon | None): The icon displayed on the button.
        font_size (int): The font size of the button text.
    """

    def __init__(
        self,
        label: str | None = None,
        icon: BootstrapIcon | None = None,
        on_click: Union[Callable[..., None], Callable[..., Awaitable[None]]] = None,
        data: str | None = None,
        type: str | None = None,
        modifier: ButtonModifier = ButtonModifier.color('primary'),
        font_size: int = 18,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a Button object.

        Args:
            label (str | None): The text label of the button.
            icon (BootstrapIcon | None): Icon of the button.
            on_click (Callable | Awaitable | None): A server-side function to handle button clicks.
            data (str | None): Additional data associated with the button.
            type (str | None): The type of the button (e.g., 'submit', 'button').
            modifier (ButtonModifier): Modifier of the button (def: ButtonModifier().color("primary")).
            font_size (int): Font size for the button text (default is 18).
            classes (list[str] | None): A list of CSS classes for the button.
            id (str | None): A unique identifier for the button.

        Raises:
            ValueError: If neither `label` nor `icon` is provided.

        Note:
            If no `id` is provided, an ID is automatically generated.
            If a callback is provided, it is automatically registered with the server.
        """
        super().__init__(classes, id)

        data = data or ''

        if label is None and icon is None:
            raise ValueError('At least one of "label" or "icon" should be provided.')

        self.label = label
        self.modifier = modifier
        self.type = type
        self.on_click = on_click or None
        self.data = data.replace("`", r"\`")
        self.icon = icon
        self.font_size = font_size

    def construct(self) -> str:
        """
        Converts the Button object into an HTML <button> element.

        Returns:
            str: The HTML code for the <button> element.
        """

        # Register the callback if provided
        if self.on_click and self.id:
            add_handler("button_click", self.id, wrap_callback(self.on_click))


        # Prepare optional attributes
        type_attr = f'type="{self.type}"' if self.type else ""
        id_attr = f'id="{self.id}"' if self.id else ""
        onclick_attr = (
            f'onclick="sendButtonClick(\'{self.id}\', false, `{self.data}`)"'
            if self.on_click
            else ""
        )

        style_attr = (
            f'style="font-size: {self.font_size}px;"'
            if self.font_size != 18
            else ""
        )

        total_label = (
            f'{self.icon.construct()} {self.label}' if self.label and self.icon
            else f'{self.label}' if self.label
            else f'{self.icon.construct()}' if self.icon
            else ''
        )

        total_class = (
            f'class="btn {self.classes_str} {self.modifier.construct()}"'
        )

        # Generate the HTML string
        return f"""
            <button {type_attr} {total_class} {style_attr} {id_attr} {onclick_attr}>
                {total_label}
            </button>
        """


class ButtonGroup(HTMLElement):
    """
    A class representing a group of HTML <button> elements, wrapped in a <div>.

    Attributes:
        buttons (list[Button]): A list of Button objects grouped together.
    """

    def __init__(
        self,
        *buttons: Button,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a ButtonGroup object.

        Args:
            buttons (list[Button]): A list of Button objects to be grouped together.
            classes (list[str] | None): A list of CSS classes for the button group.
            id (str | None): A unique identifier for the button group.
        """
        super().__init__(classes, id)
        self.buttons = buttons

    def construct(self) -> str:
        """
        Converts the ButtonGroup object into an HTML <div> containing all the buttons.

        Returns:
            str: The HTML code for the <div> element containing all the buttons in the group.
        """
        buttons_compiled = "\n".join([button.construct() for button in self.buttons])
        return f"""
        <div class="btn-group {self.classes_str}" id="{self.id if self.id else ''}">
            {buttons_compiled}
        </div>
        """
