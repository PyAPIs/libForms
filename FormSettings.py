class FormSettings:
    """ Form settings can not be update after form creation. 
    
    Attributes:
        header: str - The header to display at the top, bottom and in between elements of the form.
        default_callback: callable - The callback to run after the form concludes. This always runs before the custom callback.
        clear_form_after_action: bool - If True, the form will be cleared after an input is filled. Reduntant in OptionForm.
        clear_form_after_form: bool - If True, the form will be cleared after the form is completed.
    """

    HEADER = "header"
    DEFAULT_CALLBACK = "default_callback"
    CLEAR_FORM_AFTER_ACTION = "clear_form_after_action"
    CLEAR_FORM_AFTER_FORM = "clear_form_after_form"

    def __init__(self):
        self.settings = {
            self.HEADER: "........................................................",
            self.DEFAULT_CALLBACK: None,
            self.CLEAR_FORM_AFTER_ACTION: False,
            self.CLEAR_FORM_AFTER_FORM: False
        }

    def editSetting(self, setting, newVal=None):
        if setting not in self.settings:
            raise ValueError(f"Invalid setting: {setting}")

        if newVal is None:
            newVal = self.settings[setting]

        if setting == self.DEFAULT_CALLBACK and not callable(newVal):
            raise ValueError("default_callback must be a callable")
        elif setting in [self.CLEAR_FORM_AFTER_ACTION, self.CLEAR_FORM_AFTER_FORM] and not isinstance(newVal, bool):
            raise ValueError(f"{setting} must be a boolean")

        self.settings[setting] = newVal

    @property
    def header(self):
        return self.settings[self.HEADER]

    @property
    def default_callback(self):
        return self.settings[self.DEFAULT_CALLBACK]

    @property
    def clear_form_after_action(self):
        return self.settings[self.CLEAR_FORM_AFTER_ACTION]

    @property
    def clear_form_after_form(self):
        return self.settings[self.CLEAR_FORM_AFTER_FORM]