import os
from FormSettings import FormSettings

# Inherit this class to make edits
class Form:
    def __init__(self, title: str, body: str = None, _settings: FormSettings = None):
        """ Form class is the base class for all forms. """
        self.title = title
        self.body = body
        self.separatorCount = 0
        if _settings is None:
            print("SETTING DEFAULT SETTINGS")
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
        
        self.options[name] = {
            self._CALLBACK: callback,
            self._TOOLTIP: tooltip
        }
    
    def addSeparator(self, text: str = None) -> None:
        self.addOption(f"SEPARATOR{self.separatorCount}", lambda: text if isinstance(text, str) else "", "SEPARATOR")
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
        if self.settings.clear_form_after_action:
            print("TRIED TO CLEAR")
            os.system("cls" if os.name == "nt" else "clear")
        if self.settings.default_callback:
            self.settings.default_callback()

        self.options[chosen_option][self._CALLBACK]()

class InputForm(Form):

    # Input Consts
    TEXT = 0
    NUMBER = 1
    BOOL = 2

    # Data Consts
    TYPE = 0
    RESPONSE = 1

    def __init__(self, title: str, body: str = None, settings: object = None):
        super().__init__(title, body, settings) 
        self.inputs = {}
    
    def addInput(self, name: str, type: str = TEXT) -> None:

        if "SEPARATOR" in name and name != f"SEPARATOR{self.separatorCount}":
            raise ValueError("Option name and tooltip can not include 'SEPARATOR'")

        self.inputs[name] = {
            self.TYPE: type,
            self.RESPONSE: None
        }
    
    def addSeparator(self, text = None) -> None:
        super().addSeparator()
        self.addInput(f"SEPARATOR{self.separatorCount}", lambda: text if isinstance(text, str) else "")
    
    ## Sends the form to the user and collects their inputs. 
    def send(self) -> dict:
        super().send() 

        for name, value in self.inputs.items():
            if "SEPARATOR" in name:
                print(value[self.RESPONSE])
            elif value[self.TYPE] == self.BOOL:
                while True:
                    response = input(f"{name} (y/n): ").lower()
                    if response in ["y", "yes"]:
                        self.inputs[name][self.RESPONSE] = True
                        break 
                    elif response in ["n", "no"]:
                        self.inputs[name][self.RESPONSE] = False
                        break
                    else:
                        print("Invalid input: Please enter 'y' or 'n'.")
            elif value[self.TYPE] == self.NUMBER:
                while True:
                    try:
                        self.inputs[name][self.RESPONSE] = int(input(f"{name}: "))
                        break
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                self.inputs[name][self.RESPONSE] = input(f"{name}: ")

        print(self.settings.header)
        if self.settings.clear_form_after_action:
            print("Attempting to clear the screen...")  # Debugging line
            os.system("cls" if os.name == "nt" else "clear")
        if self.settings.default_callback:
            self.settings.default_callback()

        return self.inputs