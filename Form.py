import os
from abc import ABC

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

# Inherit this class to make edits
class Form (ABC):
    def __init__(self, title: str, body: str = None, _settings: FormSettings = None):
        """ Form class is the base class for all forms. """
        self.title = title
        self.body = body
        self.separatorCount = 0
        if _settings is None:
            self.settings = FormSettings()
        else:
            self.settings = _settings 

    def setBody(self, body: str) -> None:
        self.body = body
    
    def addSeparator(self) -> object:
        """ Adds line separator. This logic needs to be intergrated within each form.

            Use text parameter to make the separator say something instead of just a new line.
        """
        self.separatorCount += 1
    
    def send(self):
        print(self.settings.header)
        print(self.title)
        if self.body:
            print(self.body)
        print(self.settings.header)

        # Extra code here

    @property
    def settings(self) -> FormSettings:
        return self._settings
    
    @settings.setter
    def settings(self, value: FormSettings) -> None:
        if not isinstance(value, FormSettings):
            raise ValueError("settings must be an instance of FormSettings")
        self._settings = value

class OptionForm(Form):

    _CALLBACK = 0
    _TOOLTIP = 1
    
    def __init__(self, title: str, body: str = None, settings: object = None):
        super().__init__(title, body, settings) 
        self.options = {}

    def addOption(self, name: str, callback: callable, tooltip: str = None) -> None:
        """ Add an option to the form.
            
            Params:
             WARNING: name can not include "SEPARATOR"
             callback is run if the option is selected
             tooltip appears below the option for added detail. Can be blank.
        """

        if "SEPARATOR" in name and name != f"SEPARATOR{self.separatorCount}":
            raise ValueError("Option name and tooltip can not include 'SEPARATOR'")
        
        if not callable(callback):
            raise ValueError("Callback must be a callable function")
        elif callback.__code__.co_argcount not in [1, 0]:
            raise ValueError("Callback must take exactly one parameter (self) or none.")

        self.options[name] = {
            self._CALLBACK: callback,
            self._TOOLTIP: tooltip
        }
    
    def addSeparator(self, text: str = None) -> None:
        self.addOption(f"SEPARATOR{self.separatorCount}", lambda: text if text else "", "SEPARATOR")
        super().addSeparator()

    def send(self) -> None:
        super().send()

        print("Options:")
        idx = 1
        for name, value in self.options.items():
            if "SEPARATOR" in name:
                print("  " + value[self._CALLBACK]())
            else:
                tt = value[self._TOOLTIP]
                print(f"  {idx}. {name}" + (f" --> {tt}" if tt else ""))
                idx += 1

        print(self.settings.header)

        options = {key: option for key, option in self.options.items() if "SEPARATOR" not in key}

        choice = None
        while choice not in range(1, len(options) + 1):
            try:
                choice = int(input("Choose an option by number: "))
                if choice not in range(1, len(options) + 1):
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Please enter a valid number.")

        chosen_option = list(options.keys())[choice - 1]

        print(self.settings.header)
        if self.settings.clear_form_after_form:
            print("Clearing Form...")  # Debugging line
            print("\n" * 20)
            os.system("cls" if os.name == "nt" else "clear")
        if self.settings.default_callback:
            self.settings.default_callback()

        callback = self.options[chosen_option][self._CALLBACK]
        if callback.__code__.co_argcount == 1:
            callback(self)
        else:
            callback()

class InputForm(Form):

    from enum import Enum
    # Input Consts
    TEXT = 0
    NUMBER = 1
    BOOL = 2

    # Data Consts
    TYPE = 0
    RESPONSE = 1
    TOOLTIP = 2
    VALIDATION = 3
    DEFAULT = 4
    CALLBACK = 5

    class NumConsts (Enum):
        NUMTYPEKEY = 'numtype'
        NUM_INT = 'int'
        NUM_FLOAT = 'float'
        pass

    def __init__(self, title: str, body: str = None, settings: object = None):
        super().__init__(title, body, settings) 
        self.inputs = {}

    def _formInputRegisteration(func):
        def wrapper(self, name, *args, **kwargs):
            validation = kwargs.get('validation', None)
            callback = kwargs.get('callback', None)
            if "SEPARATOR" in name and name != f"SEPARATOR{self.separatorCount}":
                raise ValueError("Input name and tooltip can not include 'SEPARATOR'")
            if validation and validation.__code__.co_argcount != 1:
                raise ValueError("Validation function must take exactly one parameter (response)")
            if callback and callable(callback) and callback.__code__.co_argcount not in [1, 0]:
                raise ValueError("Callback must take exactly one parameter (self) or none.")
            
            self.inputs[name] = {
                self.RESPONSE: None,
                self.TOOLTIP: kwargs.get('tooltip', None),
            }

            return func(self, name, *args, **kwargs)
        return wrapper

    @_formInputRegisteration
    def registerTextInput(self, name: str, tooltip: str = None, validation: callable = None, default: str = None, callback: callable = None) -> None:
        """
        Args:
            name (str): The name of the input
            tooltip (str): The tooltip for the input
            validation (callable): A function that returns False if the input is valid, string explaining why otherwise
            default (str): The default value for the input
            callback (callable): A function to be called after the input is received
        """
        
        self.inputs[name][self.TYPE] = self.TEXT
        self.inputs[name][self.VALIDATION] = validation
        self.inputs[name][self.DEFAULT] = default
        self.inputs[name][self.CALLBACK] = lambda self: callback(self) if callback else None

    @_formInputRegisteration
    def registerNumberInput(self, name: str, tooltip: str = None, numType: NumConsts = NumConsts.NUM_INT, validation: callable = None, default: int = None, callback: callable = None) -> None:
        """
        Args:
            name (str): The name of the input
            tooltip (str): The tooltip for the input
            validation (callable): A function that returns False if the input is valid, string explaining why otherwise
            default (int): The default value for the input
            callback (callable): A function to be called after the input is received
        """
        
        self.inputs[name][self.NumConsts.NUMTYPEKEY] = numType
        self.inputs[name][self.TYPE] = self.NUMBER
        self.inputs[name][self.VALIDATION] = validation
        self.inputs[name][self.DEFAULT] = default
        self.inputs[name][self.CALLBACK] = lambda self: callback(self) if callback else None

    @_formInputRegisteration
    def registerBoolInput(self, name: str, tooltip: str = None, validation: callable = None, default: bool = None, callback: callable = None) -> None:
        """
        Args:
            name (str): The name of the input
            tooltip (str): The tooltip for the input
            default (bool): The default value for the input
            callback (callable): A function to be called after the input is received
        """
        def bool_validation(response: str) -> str:
            if response.lower() not in ["y", "yes", "n", "no", "true", "false"]:
                return "Invalid input: Please enter 'y' or 'n'."
            return None

        self.registerTextInput(
            name=name,
            tooltip=tooltip,
            validation=bool_validation and validation,
            callback=callback
        )
        self.inputs[name][self.TYPE] = self.BOOL
        self.inputs[name][self.DEFAULT] = default
    
    def addSeparator(self, text: str = None) -> None:
        super().addSeparator()
        self.inputs[f"SEPARATOR{self.separatorCount}"] = {
            self.TOOLTIP: str(text) if text is not None else "" 
        }

    def send(self) -> dict:
        """ 
        Sends the form to the user and collects their inputs.
        
        Note: This dictionary has the input name as a key. Best store these with constants on form creation.
        """
        super().send() 

        def clear_terminal():
            print("Clearing Form...")  # Debugging line
            print("\n" * 20)
            os.system("cls" if os.name == "nt" else "clear")

        for name, value in self.inputs.items():
            if "SEPARATOR" in name:
                print(value[self.TOOLTIP])
                continue
            
            inputCode = lambda: input(
                name
                + (f" (Default: {value[self.DEFAULT]})" if value[self.DEFAULT] is not None else "")
                + (f" --> {value[self.TOOLTIP]}" if value[self.TOOLTIP] else "")    
                + (" (y/n)" if value[self.TYPE] == self.BOOL else "") 
                + ": "
            )

            if value[self.TYPE] == self.BOOL:
                while True:
                    response = inputCode().lower()
                    if response in ["y", "yes", "true"]:
                        self.inputs[name][self.RESPONSE] = True
                    elif response in ["n", "no", "false"]:
                        self.inputs[name][self.RESPONSE] = False
                    elif response == "" and value[self.DEFAULT] is not None:
                        self.inputs[name][self.RESPONSE] = value[self.DEFAULT]
                    else:
                        print("Invalid input: Please enter 'y' or 'n'.")
                        continue

                    if value[self.VALIDATION]:
                        validation_result = value[self.VALIDATION](self.inputs[name][self.RESPONSE])
                        if validation_result:
                            print(validation_result)
                            continue
                    break
            elif value[self.TYPE] == self.NUMBER:
                ERROR_INV_NUMCONST = 'err_invalid-numconst'

                while True:
                    try:
                        response = inputCode()
                        if response == "" and value[self.DEFAULT] is not None:
                            self.inputs[name][self.RESPONSE] = value[self.DEFAULT]
                            break
                        
                        numType = value[self.NumConsts.NUMTYPEKEY]
                        response = float(response)
                        if (numType == self.NumConsts.NUM_FLOAT):
                            pass
                        elif (numType == self.NumConsts.NUM_INT):
                            response = round(response)
                        else:
                            raise ValueError(ERROR_INV_NUMCONST) # This will be ignored because of the try-catch block

                        if value[self.VALIDATION]:
                            validation_result = value[self.VALIDATION]((response))
                            if validation_result:
                                print(validation_result)
                                continue
                        self.inputs[name][self.RESPONSE] = response
                        break
                    except ValueError as e:
                        if str(e) == ERROR_INV_NUMCONST:
                            print("WARNING Developer Error: numType not a NumConst")
                        else:
                            print("Please enter a valid number.")
            else:
                while True:
                    response = inputCode()
                    if response == "" and value[self.DEFAULT] is not None:
                        self.inputs[name][self.RESPONSE] = value[self.DEFAULT]
                        break

                    if value[self.VALIDATION]:
                        validation_result = value[self.VALIDATION](response)
                        if validation_result:
                            print(validation_result)
                            continue
                    self.inputs[name][self.RESPONSE] = response
                    break

            if self.settings.clear_form_after_action:
                clear_terminal()
            callback = value.get(self.CALLBACK, None)
            if callback and callable(callback):
                if callback.__code__.co_argcount == 1:
                    callback(self)
                else:
                    callback()

        if self.settings.clear_form_after_form:
            clear_terminal()
        print(self.settings.header)
        if self.settings.default_callback:
            self.settings.default_callback()

        for name in list(self.inputs.keys()): # Remove separators from response
            if "SEPARATOR" in name:
                self.inputs.pop(name)

        return self.inputs