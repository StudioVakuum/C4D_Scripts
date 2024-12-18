"""
SV Create Folder Path

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Create a string of the selected folder path

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d
import os

class MyDialog(c4d.gui.GeDialog):
    ID_INPUT = 1000

    def __init__(self):
        super().__init__()
        self.result = None

    def CreateLayout(self):
        self.SetTitle("Add Name to String")
        self.AddStaticText(1001, c4d.BFH_LEFT, 300, 0, "Write Name:")
        self.AddEditText(self.ID_INPUT, c4d.BFH_SCALEFIT, 0, 0)
        self.SetString(self.ID_INPUT, "Folder Path")
        self.GroupBegin(1000, c4d.BFH_SCALEFIT, 2, 1, "Actions")
        self.AddButton(2002, c4d.BFH_SCALEFIT, name="Cancel")
        self.AddButton(2003, c4d.BFH_SCALEFIT, name="Add")
        self.GroupEnd()
        return True

    def Command(self, id, msg):
        if id == 2003:
            self.result = self.GetString(self.ID_INPUT)
            self.Close()
        elif id == 2002:
            self.result = None
            self.Close()
        return True

    def Message(self, msg, result):
        bc = c4d.BaseContainer()
        ok = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if ok and bc[c4d.BFM_INPUT_VALUE] == 1:
            self.Command(2003, None)
            return True
        ok = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if ok and bc[c4d.BFM_INPUT_VALUE] == 1:
            self.Command(2002, None)
            return True
        return super().Message(msg, result)

def main():
    doc = c4d.documents.GetActiveDocument()
    project_path = doc.GetDocumentPath()
    
    obj = doc.GetActiveObject()

    if obj is None:
        c4d.gui.MessageDialog("Please select an object.")
        return

    if not project_path:
        c4d.gui.MessageDialog("The document is not saved yet.")
        return

    project_path = os.path.normpath(project_path)

    selected_folder = c4d.storage.LoadDialog(type=c4d.FILESELECT_DIRECTORY, title="Select Folder", flags=c4d.FILESELECT_DIRECTORY, def_path=project_path)

    if not selected_folder:
        c4d.gui.MessageDialog("No folder selected.")
        return

    selected_folder = os.path.normpath(selected_folder)

    dialog = MyDialog()
    dialog.Open(c4d.DLG_TYPE_MODAL, 0)

    name = dialog.result

    if name is None:
        return

    bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_DEFAULT] = selected_folder

    userdata_id = obj.AddUserData(bc)
    obj.SetParameter(userdata_id, selected_folder, c4d.DESCFLAGS_SET_0)

    c4d.EventAdd()

if __name__ == '__main__':
    main()