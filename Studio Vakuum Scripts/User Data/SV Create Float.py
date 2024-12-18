"""
SV Create Float

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Create float for user data

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

class MyDialog(c4d.gui.GeDialog):
    ID_INPUT = 1000
    ID_UNIT = 1001

    def __init__(self):
        super().__init__()
        self.result = None
        self.selected_unit = None

    def CreateLayout(self):
        self.SetTitle("Add Name to Float")
        self.AddStaticText(1002, c4d.BFH_LEFT, 300, 0, "Write Name:")
        self.AddEditText(self.ID_INPUT, c4d.BFH_SCALEFIT, 0, 0)
        self.SetString(self.ID_INPUT, "Float Name")

        self.AddStaticText(1003, c4d.BFH_LEFT, 300, 0, "Select Unit:")
        self.AddComboBox(self.ID_UNIT, c4d.BFH_SCALEFIT, 0, 0)
        self.AddChild(self.ID_UNIT, 0, "None")
        self.AddChild(self.ID_UNIT, 1, "Length Unit")
        self.AddChild(self.ID_UNIT, 2, "Percent")
        self.AddChild(self.ID_UNIT, 3, "Degree")

        self.GroupBegin(2000, c4d.BFH_SCALEFIT, 2, 1, "Actions")
        self.AddButton(2002, c4d.BFH_SCALEFIT, name="Cancel")
        self.AddButton(2003, c4d.BFH_SCALEFIT, name="Add")
        self.GroupEnd()

        return True

    def Command(self, id, msg):
        if id == 2003:
            self.result = self.GetString(self.ID_INPUT)
            self.selected_unit = self.GetInt32(self.ID_UNIT)
            self.Close()
        elif id == 2002:
            self.result = None
            self.selected_unit = None
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
    selected_unit = dialog.selected_unit

    if name is None:
        return

    unit_map = {
        0: c4d.DESC_UNIT_FLOAT,
        1: c4d.DESC_UNIT_METER,
        2: c4d.DESC_UNIT_PERCENT,
        3: c4d.DESC_UNIT_DEGREE
    }

    unit = unit_map.get(selected_unit, c4d.DESC_UNIT_FLOAT)

    bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_REAL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_UNIT] = unit

    obj.AddUserData(bc)
    c4d.EventAdd()

if __name__ == '__main__':
    main()