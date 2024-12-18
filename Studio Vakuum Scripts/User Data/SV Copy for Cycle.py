"""
SV Copy for Cycle

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Select the objects or materials to copy their names and format it in clipboard before using for the script "SV Create Cycle from Clipboard".

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d
from c4d import gui

def main():
    # Get selected objects
    selection = doc.GetSelection()
    # Get selected materials
    selected_materials = doc.GetActiveMaterials()

    # Check if both objects and materials are selected
    if selection and selected_materials:
        gui.MessageDialog("You can only select either objects or materials, not both.")
        return

    # Check if nothing is selected
    if not selection and not selected_materials:
        gui.MessageDialog("No Objects or Materials selected.")
        return

    name_list = ""

    # If only objects are selected
    if selection:
        for index, obj in enumerate(selection):
            name_list += f"{index};{obj.GetName()}\n"

    # If only materials are selected
    if selected_materials:
        for index, mat in enumerate(selected_materials):
            name_list += f"{index};{mat.GetName()}\n"

    # Copy names to clipboard
    c4d.CopyStringToClipboard(name_list)

    # Display message
    gui.MessageDialog("Names have been copied to the clipboard. You can now paste them into a Cycle text field inside of 'Manage User Data'.")

if __name__ == '__main__':
    main()
