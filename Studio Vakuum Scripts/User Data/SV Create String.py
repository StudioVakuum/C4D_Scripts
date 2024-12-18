"""
SV Create String

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Create string for user data

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

class MyDialog(c4d.gui.GeDialog):

    ID_INPUT = 1000

    def __init__(self):
        super().__init__()
        self.result = None 

    def CreateLayout(self):
        self.SetTitle("Add Name to String")
        self.AddStaticText(1001, c4d.BFH_LEFT, 300, 0, "Write Name:")
        self.AddEditText(self.ID_INPUT, c4d.BFH_SCALEFIT, 0, 0)
        self.SetString(self.ID_INPUT, "String Name")
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
    obj = c4d.documents.GetActiveDocument().GetActiveObject()

    if obj is None:
        c4d.gui.MessageDialog("Please select an object.")
        return

    dialog = MyDialog()
    dialog.Open(c4d.DLG_TYPE_MODAL, 0) 

    name = dialog.result

    if name is None:
        return  

    bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING)
    bc[c4d.DESC_NAME] = name

    obj.AddUserData(bc)
    c4d.EventAdd()

if __name__ == '__main__':
    main()