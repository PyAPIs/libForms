from Form import *

class OptionFormExample:

    settings = FormSettings()
    settings.editSetting(FormSettings.Setting.HEADER, "+-+-+-+-+-+-+-+-+-")
    settings.editSetting(FormSettings.Setting.SEPARATOR, "/*******************\\")
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)
    settings.editSetting(FormSettings.Setting.DEFAULT_CALLBACK, lambda: print("Default callback"))
    settings.editSetting(FormSettings.Setting.OPTIONS_TEXT, "Pick an option!!!")

    form = OptionForm(
        title="Form Title",
        body="This is a form with three options.",
        settings=settings # Displays assigning settings after during creation
    )

    form.addOption(
        name="Option 1",
        callback=lambda: print("Option 1 selected")
    )
    form.addOption(
        name="Option 2",
        callback=lambda: print("Option 2 selected"),
        tooltip="This is a tooltip for Option 2"
    )

    form.addSeparator()

    form.addOption(
        name="Option 3",
        callback=lambda: print("Option 3 selected")
    )

    form.addSeparator("This is a separator with a tooltip")

    form.send()

class InputFormExample:
    form = InputForm(
        title="Form Title",
        body="This is a form with three inputs."
    )

    settings = FormSettings()
    settings.editSetting(FormSettings.Setting.HEADER, "\\/\/\/\/\/\/\/\/\/")
    settings.editSetting(FormSettings.Setting.SEPARATOR, "/*******************\\" + "\n" + "\\*******************/")
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)
    settings.editSetting(FormSettings.Setting.DEFAULT_CALLBACK, lambda: print("\nValue Entered\n"))

    form.settings = settings # Displays assigning settings after form creation
    
    form.registerTextInput(
        name="Text Input",
        tooltip="This is a tooltip for Text input",
        callback=lambda self: self.settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_ACTION, True)
    )

    form.registerBoolInput(
        name="Bool input",
        tooltip="This is a tooltip for Bool input",
        default=True
    )

    form.addSeparator()

    form.registerNumberInput(
        name="Number Input",
        tooltip="This is a tooltip for Number input",
        numType=InputForm.NumConsts.NUM_FLOAT
    )

    response = form.send()

    print("\n\nResponse:")
    for key, value in response.items():
        print(f"{key}: {value.get(InputForm.DataEntryConsts.RESPONSE, 'No response')} ({type(value.get(InputForm.DataEntryConsts.RESPONSE, None))})")