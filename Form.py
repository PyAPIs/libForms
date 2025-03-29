import os
from abc import ABC
from enum import Enum
from click import style
from colorama import Fore, Style

class FormSettings:
    """ This class is used to customise forms and give them their own look and feel.
    
    Attributes:
        - header `str` - The header to display at the top and bottom of a form.
        - separator `str` - String to be displayed in between elements of a form.
        - default_callback `callable` - The callback to run after the form concludes. This always runs before the custom callback.
        - clear_form_after_action `bool` - If True, the form will be cleared after an input is filled. Reduntant in OptionForm.
        - clear_form_after_form `bool` - If True, the form will be cleared after the form is completed.
    """

    class Setting (Enum):
        """ Enum class storing setting types. """
        HEADER = 0
        SEPARATOR = 1
        DEFAULT_CALLBACK = 2
        CLEAR_FORM_AFTER_ACTION = 3
        CLEAR_FORM_AFTER_FORM = 4

        ERROR_COLOUR = 5
        OPTIONS_TEXT = 6
        pass

    def __init__(self) -> None:
        self.settings = { # Initialises default settings
            self.Setting.HEADER: "........................................................",
            self.Setting.SEPARATOR: "",
            self.Setting.DEFAULT_CALLBACK: None,
            self.Setting.CLEAR_FORM_AFTER_ACTION: False,
            self.Setting.CLEAR_FORM_AFTER_FORM: False,
            self.Setting.ERROR_COLOUR: Fore.RED,
            self.Setting.OPTIONS_TEXT: "Options"
        }

    def editSetting(self, setting: Setting, newVal):
        """ Edits the value of a form setting.

        Attributes:
            - setting `FormSettings.Setting` - The setting you want edited (retrieved from the referal consts).
            - newVal `Any` - The new value you want to replace the setting with. Must adhere to the rules listed below. 
        """

        # Validation that setting exists
        if not isinstance(setting, self.Setting) or setting not in self.settings:
            raise ValueError(f"Invalid setting: {setting}")

        # Validation for newVal's
        if setting == self.Setting.DEFAULT_CALLBACK and not callable(newVal):
            raise ValueError("default_callback must be a callable")
        elif setting in [self.Setting.CLEAR_FORM_AFTER_ACTION, self.Setting.CLEAR_FORM_AFTER_FORM] and not isinstance(newVal, bool):
            raise ValueError(f"{setting} must be a boolean")
        elif setting in [self.Setting.HEADER, self.Setting.SEPARATOR] and not isinstance(newVal, str):
            raise ValueError(f"{setting} must be a string")

        self.settings[setting] = newVal # Sets setting to newVal

    def getSetting(self, setting: Setting):
        """ Returns an `any` value of a form setting.

        Attributes:
            - setting `Any` - The setting you want changed (retrieved from the referal consts).

        Returns a ValueError if the setting does not exist.
        """
        # Validation that setting exists
        if not isinstance(setting, self.Setting) or setting not in self.settings:
            raise ValueError(f"Invalid setting: {setting}")
        
        return self.settings[setting] # Returns query

class Form (ABC):
    def __init__(self, title: str, body: str = None, _settings: FormSettings = None):
        """ This class is the base class for all forms. 
        
        Attributes:
            - title `str` - Titles the form. This title is displayed first.
            - body `str` - (Optional) Provide extra information to the form.
            - settings `FormSettings` - (Optional) Settings for customisation. Import it here if you are using a standardised settings book.
        """
        self.title = title + Style.RESET_ALL
        self.body = body + Style.RESET_ALL if body else None
        self.separatorCount = 0 # Set to zero. This variable is counted to ensure every separator has a unique name.
        if _settings is None:
            self.settings = FormSettings() # Sets settings to a default configuration if no custom settings were provided.
        else:
            self.settings = _settings 

    def setBody(self, body: str) -> None:
        self.body = body + Style.RESET_ALL
    
    def addSeparator(self) -> object:
        """ Adds line separator. This logic needs to be intergrated within each form.

        Use text parameter to make the separator say something instead of just a new line.
        """
        self.separatorCount += 1
        pass
    
    def send(self):
        """ Sends the form to the user.
        
        The code displayed here is what will be displayed prior to the form information.
        """
        print(self.settings.getSetting(FormSettings.Setting.HEADER))
        print(self.title)
        if self.body:
            print(self.body)
        print(self.settings.getSetting(FormSettings.Setting.SEPARATOR))

        # Extra code here
        pass

    @property
    def settings(self) -> FormSettings:
        """ Get form settings """
        return self._settings
    
    @settings.setter
    def settings(self, value: FormSettings) -> None:
        """ Override form settings 
        
        You do not need to override settings each time you want to edit an attribute. Unless you have a settings class stored in a constant variable, use form.settings.editSetting() to create edits.
        """
        if not isinstance(value, FormSettings):
            raise ValueError("settings must be an instance of FormSettings")
        self._settings = value

class OptionForm(Form):

    # Constants used to save option attributes
    _CALLBACK = 0
    _TOOLTIP = 1
    
    def __init__(self, title: str, body: str = None, settings: FormSettings = None):
        super().__init__(title, body, settings) 
        self.options = {} # Initialises an empty set of options.

    def addOption(self, name: str, callback: callable, tooltip: str = None) -> None:
        """ Add an option to the form.
            
            Params:
             WARNING: name can not include "SEPARATOR"
             callback is run if the option is selected
             tooltip appears below the option for added detail. Can be blank.
        """

        if "SEPARATOR" in name and not "SEPARATOR" in tooltip: # Disallow "SEPARATOR" to be in the name of any option. This is to prevent any future errors. 
            raise ValueError("Option name and tooltip can not include 'SEPARATOR'")
        
        if not callable(callback): # Ensure callback is a callable.
            raise ValueError("Callback must be a callable function")

        # Adds option to the dictionary.
        self.options[name] = {
            self._CALLBACK: callback,
            self._TOOLTIP: tooltip
        }
    
    def addSeparator(self, text: str = None) -> None:
        """ Create a separator between options. """
        super().addSeparator()
        self.addOption(f"SEPARATOR{self.separatorCount}", lambda: text + Style.RESET_ALL if text else "", "SEPARATOR") # lambda returns text if text exists.

    def send(self) -> None:
        super().send()

        print(f"{self.settings.getSetting(FormSettings.Setting.OPTIONS_TEXT)}:")
        idx = 1 # Index to signify the order of the options.
        options = {}  # A local variable with no separators and only options.
        for name, value in self.options.items(): # Separates self.options into its key (name) and a info dict
            if "SEPARATOR" in name:
                print("  " + value[self._CALLBACK]()) # Prints separator text (if it exists)
            else: # Print option
                tt = value[self._TOOLTIP] # Get value for tooltip
                print(f"  {idx}. {name}" + (f" --> {tt + Style.RESET_ALL}" if tt else "") + Style.RESET_ALL) # Print option in form `index. Option --> tooltip`
                idx += 1 # Add to index
                options[name] = value

        print(self.settings.getSetting(FormSettings.Setting.SEPARATOR))

        choice = None # Assign None to choice to enter while loop.
        while choice not in range(1, len(options) + 1): # Validation to ensure a valid option was selected
            try:
                choice = int(input("Choose an option by number: ")) # Converts input to integer
                if choice not in range(1, len(options) + 1): # True if the choice is not in the bounds of the options
                    print(self.settings.getSetting(FormSettings.Setting.ERROR_COLOUR) + "Invalid choice, please try again." + Style.RESET_ALL)
            except ValueError: # Catches cases where an int is not inputted in choice. Returns error and reruns while loop.
                print(self.settings.getSetting(FormSettings.Setting.ERROR_COLOUR) + "Please enter a valid number." + Style.RESET_ALL)

        chosen_option = list(options.keys())[choice - 1] # Get the selected option.

        print(self.settings.getSetting(FormSettings.Setting.HEADER))
        if self.settings.getSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM):
            print("Clearing Form...")  # Debugging line
            print("\n" * 20) # Separator line if the system can not clear the console.
            os.system("cls" if os.name == "nt" else "clear")
        if self.settings.getSetting(FormSettings.Setting.DEFAULT_CALLBACK):
            self.settings.getSetting(FormSettings.Setting.DEFAULT_CALLBACK)() # Run form callback.

        # Run the callback of the selected option.
        callback = self.options[chosen_option][self._CALLBACK]
        if callback.__code__.co_argcount == 1: # Return true if callback is passing exactly one parameter. 
            callback(self) # Send in `self` as a parameter if the callback requires it.
        else:
            callback() # Otherwise, just call callback

class InputForm(Form):

    class InputConsts (Enum):
        """ Enum class defining what types of compatible inputs """
        TEXT = 0
        NUMBER = 1
        BOOL = 2
        pass

    class DataEntryConsts (Enum):
        """ Enum class defining the data within an input """
        TYPE = 0
        RESPONSE = 1
        TOOLTIP = 2
        VALIDATION = 3
        DEFAULT = 4
        CALLBACK = 5
        pass

    class NumConsts (Enum):
        """ Enum class defining type of output a numeric input should be converted to """
        NUMTYPEKEY = 'numtype' # Key for number types. String to avoid overwriting.
        NUM_INT = 0
        NUM_FLOAT = 1
        pass

    def __init__(self, title: str, body: str = None, settings: FormSettings = None):
        super().__init__(title, body, settings) 
        self.inputs = {}

    def _formInputRegistration(func):
        """ Decorator used to register the default data.
        
        Validates:
            - The input name does not contain 'SEPARATOR' (prevents separator identification conflicts)
            - The validation function (if provided) takes exactly one argument (response).
            - The callback function (if provided) takes either zero or one argument (nothing or self).
    """
        def wrapper(self, name, *args, **kwargs):
            validation = kwargs.get('validation', None) # Gets the value for the (keyword) parameter validation
            callback = kwargs.get('callback', None) # Gets the value for the (keyword) parameter validation
            if "SEPARATOR" in name:
                raise ValueError("Input name and tooltip cannot include 'SEPARATOR'") # Disallow "SEPARATOR" to be in the name of any option. This is to prevent any future errors. 
            if validation and validation.__code__.co_argcount != 1: # If validation exists, checks that the callable has at least one parameter.
                raise ValueError("Validation function must take at least one parameter (response)")
            
            self.inputs[name] = { # Saves the necessary data to Inputs. This will be expanded by the functions this is decorating.
                self.DataEntryConsts.RESPONSE: None,
                self.DataEntryConsts.TOOLTIP: kwargs.get('tooltip', None), # Assign TOOLTIP from the tooltip parameter from the function/
            }

            return func(self, name, *args, **kwargs)
        return wrapper

    @_formInputRegistration
    def registerTextInput(self, name: str, tooltip: str = None, validation: callable = None, default: str = None, callback: callable = None) -> None:
        """
        Args:
            name (str): The name of the input
            tooltip (str): The tooltip for the input
            validation (callable): A function that returns False if the input is valid, string explaining why otherwise
            default (str): The default value for the input
            callback (callable): A function to be called after the input is received
        """
        
        self.inputs[name][self.DataEntryConsts.TYPE] = self.InputConsts.TEXT
        self.inputs[name][self.DataEntryConsts.VALIDATION] = validation
        self.inputs[name][self.DataEntryConsts.DEFAULT] = default
        self.inputs[name][self.DataEntryConsts.CALLBACK] = callback

    @_formInputRegistration
    def registerNumberInput(self, name: str, tooltip: str = None, numType: NumConsts = NumConsts.NUM_INT, validation: callable = None, default: float = None, callback: callable = None) -> None:
        """
        Args:
            name (str): The name of the input
            tooltip (str): The tooltip for the input
            validation (callable): A function that returns False if the input is valid, string explaining why otherwise
            default (int): The default value for the input
            callback (callable): A function to be called after the input is received
        """
        
        self.inputs[name][self.NumConsts.NUMTYPEKEY] = numType
        self.inputs[name][self.DataEntryConsts.TYPE] = self.InputConsts.NUMBER
        self.inputs[name][self.DataEntryConsts.VALIDATION] = validation
        self.inputs[name][self.DataEntryConsts.DEFAULT] = default
        self.inputs[name][self.DataEntryConsts.CALLBACK] = callback

    @_formInputRegistration
    def registerBoolInput(self, name: str, tooltip: str = None, default: bool = None, callback: callable = None) -> None:
        """
        Args:
            name (str): The name of the input
            tooltip (str): The tooltip for the input
            default (bool): The default value for the input
            callback (callable): A function to be called after the input is received
        """

        self.registerTextInput(
            name=name,
            tooltip=tooltip,
            callback=callback
        )
        self.inputs[name][self.DataEntryConsts.TYPE] = self.InputConsts.BOOL
        self.inputs[name][self.DataEntryConsts.DEFAULT] = default
    
    def addSeparator(self, text: str = None) -> None:
        super().addSeparator()
        self.inputs[f"SEPARATOR{self.separatorCount}"] = {
            self.DataEntryConsts.TOOLTIP: str(text) if text is not None else "" 
        }

    def send(self) -> dict:
        """ 
        Sends the form to the user and collects their inputs.
        
        Note: This dictionary has the input name as a key. Best store these with constants on form creation.
        """
        super().send() 

        def clear_terminal():
            print("Clearing Form...")  # Debugging line
            print("\n" * 20) # Separator line if the system can not clear the console.
            os.system("cls" if os.name == "nt" else "clear")

        for name, data in self.inputs.items():
            if "SEPARATOR" in name:
                print(data[self.DataEntryConsts.TOOLTIP]) # Print separator
                continue # Skip to next iteration
            
            inputCode = lambda: input( # Anonomous function to format the input.
                name
                + (f" (Default: {data[self.DataEntryConsts.DEFAULT]})" if data[self.DataEntryConsts.DEFAULT] is not None else "")
                + (f" --> {data[self.DataEntryConsts.TOOLTIP]}" if data[self.DataEntryConsts.TOOLTIP] else "")    
                + (" (y/n)" if data[self.DataEntryConsts.TYPE] == self.InputConsts.BOOL else "") 
                + ": "
                + Style.RESET_ALL
            )

            if data[self.DataEntryConsts.TYPE] == self.InputConsts.BOOL:
                while True: # Repeat until a valid value is outputted
                    response = inputCode().lower()
                    if response in ["y", "yes", "true"]: # Handle true cases
                        self.inputs[name][self.DataEntryConsts.RESPONSE] = True
                    elif response in ["n", "no", "false"]: # Handle false cases
                        self.inputs[name][self.DataEntryConsts.RESPONSE] = False
                    elif response == "" and data[self.DataEntryConsts.DEFAULT] is not None: # Handle empty cases where a default value exists
                        self.inputs[name][self.DataEntryConsts.RESPONSE] = data[self.DataEntryConsts.DEFAULT]
                    else: # Handle invalid cases
                        print(self.settings.getSetting(FormSettings.Setting.ERROR_COLOUR) + "Invalid input: Please enter 'y' or 'n'." + Style.RESET_ALL)
                        continue # Try again

                    break # Skip to next iteration
            elif data[self.DataEntryConsts.TYPE] == self.InputConsts.NUMBER:
                ERROR_INV_NUMCONST = 'err_invalid-numconst' # Error const for easier one-time translation.

                while True: # Repeat until a valid value is outputted
                    try:
                        response = inputCode()
                        if response == "" and data[self.DataEntryConsts.DEFAULT] is not None: # Replace empty values with default 
                            self.inputs[name][self.DataEntryConsts.RESPONSE] = data[self.DataEntryConsts.DEFAULT]
                            break # Skip to next iteration
                        
                        numType = data[self.NumConsts.NUMTYPEKEY] # Get the number type (float or int) the number needs to be converted to.
                        response = float(response)
                        if (numType == self.NumConsts.NUM_FLOAT):
                            pass # Already converted to a float :)
                        elif (numType == self.NumConsts.NUM_INT):
                            response = round(response) # Rounds to nearest value and converts to a string.
                        else:
                            raise ValueError(ERROR_INV_NUMCONST) # This will be ignored because of the try-catch block

                        if data[self.DataEntryConsts.VALIDATION]: # Execute validation (if exists)
                            validation_result = data[self.DataEntryConsts.VALIDATION]((response))
                            if validation_result: # If validation is True (i.e. not None), the validation has failed.
                                print(self.settings.getSetting(FormSettings.Setting.ERROR_COLOUR + validation_result + Style.RESET_ALL)) # Print error
                                continue # Try again
                        self.inputs[name][self.DataEntryConsts.RESPONSE] = response
                        break # Skip to next iteration
                    except ValueError as e:
                        if str(e) == ERROR_INV_NUMCONST:
                            raise ValueError(self.settings.getSetting(FormSettings.Setting.ERROR_COLOUR) + f"numType {str(data[self.NumConsts.NUMTYPEKEY])} not a NumConst" + Style.RESET_ALL)
                        else:
                            print(self.settings.getSetting(FormSettings.Setting.ERROR_COLOUR) + "Please enter a valid number." + Style.RESET_ALL)
            else: # Case where the type is text. 
                while True: # Repeat until a valid value is outputted
                    response = inputCode()
                    if response == "" and data[self.DataEntryConsts.DEFAULT] is not None: # Replace empty values with default
                        self.inputs[name][self.DataEntryConsts.RESPONSE] = data[self.DataEntryConsts.DEFAULT]
                        break # Skip to next iteration

                    if data[self.DataEntryConsts.VALIDATION]: # Execute validation (if exists)
                        validation_result = data[self.DataEntryConsts.VALIDATION](response)
                        if validation_result: # If validation is True (i.e. not None), the validation has failed.
                            print(self.settings.getSetting(FormSettings.Setting.ERROR_COLOUR) + validation_result + Style.RESET_ALL) # Print error
                            continue # Try again
                    self.inputs[name][self.DataEntryConsts.RESPONSE] = response
                    break # Skip to next iteration

            if self.settings.getSetting(FormSettings.Setting.CLEAR_FORM_AFTER_ACTION):
                clear_terminal()
            callback = data.get(self.DataEntryConsts.CALLBACK, None)
            if callback and callable(callback):
                if callback.__code__.co_argcount == 1:
                    callback(self) # Pass through self if callback has one parameter
                else:
                    callback()

        if self.settings.getSetting(FormSettings.Setting.DEFAULT_CALLBACK):
            self.settings.getSetting(FormSettings.Setting.DEFAULT_CALLBACK)() # If default callback is given, run it.
        print(self.settings.getSetting(FormSettings.Setting.HEADER)) # Print header at the end.
        if self.settings.getSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM):
            clear_terminal() # Clear terminal

        for name in list(self.inputs.keys()): # Remove separators from response
            if "SEPARATOR" in name:
                self.inputs.pop(name)

        return self.inputs # Return all inputs for manipulation.