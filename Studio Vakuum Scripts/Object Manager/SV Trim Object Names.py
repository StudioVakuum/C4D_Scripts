"""
SV Trim Object Names

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Removes a specified number of characters from the beginning or end of selected object names.

Written for Maxon Cinema 4D 2026.2.0 or later
Python version 3.11.4
"""

import c4d

class TrimDialog(c4d.gui.GeDialog):
    ID_AMOUNT = 1000
    ID_MODE = 1001

    def __init__(self):
        super().__init__()
        self.amount = None
        self.mode = None

    def CreateLayout(self):
        self.SetTitle("Trim Object Names")

        # --- ROW 1: Amount ---
        self.GroupBegin(3000, c4d.BFH_SCALEFIT, 2, 1)
        self.AddStaticText(1002, c4d.BFH_LEFT, name="Chars:")
        self.AddEditNumberArrows(self.ID_AMOUNT, c4d.BFH_LEFT, 80, 0)
        self.SetInt32(self.ID_AMOUNT, 3)
        self.GroupEnd()

        # --- ROW 2: Radio ---
        self.GroupBegin(3001, c4d.BFH_SCALEFIT, 2, 1)
        self.AddStaticText(1003, c4d.BFH_LEFT, name="Trim:")

        self.AddRadioGroup(self.ID_MODE, c4d.BFH_LEFT, 2, 1)
        self.AddChild(self.ID_MODE, 0, "Start")
        self.AddChild(self.ID_MODE, 1, "End")
        self.SetInt32(self.ID_MODE, 0)

        self.GroupEnd()

        # --- Buttons ---
        self.GroupBegin(2000, c4d.BFH_RIGHT, 2, 1)
        self.AddButton(2002, c4d.BFH_SCALEFIT, name="Cancel")
        self.AddButton(2003, c4d.BFH_SCALEFIT, name="Apply")
        self.GroupEnd()

        return True

    def Command(self, id, msg):
        if id == 2003:
            self.amount = self.GetInt32(self.ID_AMOUNT)
            self.mode = self.GetInt32(self.ID_MODE)
            self.Close()

        elif id == 2002:
            self.amount = None
            self.mode = None
            self.Close()

        return True


def trim_name(name, amount, from_start):
    if amount <= 0:
        return name
    return name[amount:] if from_start else name[:-amount] if amount < len(name) else ""


def main():
    doc = c4d.documents.GetActiveDocument()
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    if not selection:
        c4d.gui.MessageDialog("No objects selected.")
        return

    dlg = TrimDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL)

    if dlg.amount is None:
        return

    amount = dlg.amount
    from_start = (dlg.mode == 0)

    doc.StartUndo()

    for obj in selection:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.SetName(trim_name(obj.GetName(), amount, from_start))

    doc.EndUndo()
    c4d.EventAdd()


if __name__ == "__main__":
    main()