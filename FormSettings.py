class FormSettings:
    """ Form settings can not be update after form creation. 
    
    Attributes:
        header: str - The header to display at the top, bottom and in between elements of the form.
        default_callback: callable - The callback to run after the form concludes. This always runs before the custom callback.
        clear_form_after_action: bool - If True, the form will be cleared after an option is selected.
    """

    def __init__(self):
        self.header = "........................................................"
        self._default_callback = None
        self._clear_form_after_action = False

    @property
    def default_callback(self):
        return self._default_callback

    @default_callback.setter
    def default_callback(self, value: callable):
        if not callable(value):
            raise ValueError("default_callback must be a callable")
        self._default_callback = value

    @property
    def clear_form_after_action(self):
        return self._clear_form_after_action

    @clear_form_after_action.setter
    def clear_form_after_action(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("clear_form_after_action must be a boolean")
        self._clear_form_after_action = value