from kivy.factory import Factory

# Alias for the register function from Factory
register = Factory.register

"""
Registers custom components to the Kivy Factory.

This code registers each component within the "ui" directory to the Kivy Factory. 
Once registered, the components can be used without explicitly importing them elsewhere in the kvlang files.
"""

# Register the component with Kivy's Factory
register("CButton", module="carbonkivy.ui.button")
register("CTextInput", module="carbonkivy.ui.textinput")
register("CDropdown", module="carbonkivy.ui.dropdown")
register("CDatePicker", module="carbonkivy.ui.datepicker")
