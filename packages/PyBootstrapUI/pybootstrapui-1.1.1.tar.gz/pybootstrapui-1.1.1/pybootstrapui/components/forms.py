from .base import HTMLElement


class Form(HTMLElement):
    """
    A class representing an HTML <form> element with child elements, action, and method attributes.

    Attributes:
        child (list[HTMLElement]): A list of child elements to include inside the form.
        action (str): The URL to which the form data will be sent when submitted.
        action_type (str): The HTTP method for form submission (default is 'GET').
        classes (list[str] | None): Optional list of classes to apply to the form element.
        id (str | None): Optional unique ID for the form element.
    """

    def __init__(
        self,
        *child_elements: HTMLElement,
        action: str,
        action_type: str = "GET",
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes the Form object with specified child elements, action, and method type.

        Args:
            child_elements (HTMLElement): The child elements to include inside the form.
            action (str): The action URL for the form submission.
            action_type (str): The HTTP method for form submission (GET/POST). Defaults to 'GET'.
            classes (list[str] | None): Optional list of classes for the form element.
            id (str | None): Optional unique ID for the form element.

        Example:
            form = Form(
                InputField(),
                Button("Submit"),
                action="/submit",
                action_type="POST",
                classes=["form-class"]
            )
        """
        super().__init__(classes, id)
        self.child = child_elements
        self.action = action
        self.action_type = action_type

    def construct(self) -> str:
        """
        Generates the HTML for the form element with its action, method, and child elements.

        Returns:
            str: The HTML code for the form element.

        Example:
            html = form.construct()
            print(html)
        """
        compiled_child = "\n".join([child.construct() for child in self.child])
        id_attr = f'id="{self.id}"' if self.id else ""
        return f"""
        <form action="{self.action}" method="{self.action_type}" class="{self.classes_str}" {id_attr}>
            {compiled_child}
        </form>
        """
