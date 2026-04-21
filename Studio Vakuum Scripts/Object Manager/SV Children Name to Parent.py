"""
SV Children Name to Parent

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Apply name of the selected child objects to their parents based on levels up.

Written for Maxon Cinema 4D 2026.2.0
Python version 3.11.4
"""

import c4d
from c4d import gui

class RenameHierarchyDialog(gui.GeDialog):
    def __init__(self):
        super().__init__()
        self.user_input = None
        self.add_suffix = False

    def CreateLayout(self):
        self.SetTitle("Children Name to Parent")

        self.AddStaticText(1000, c4d.BFH_LEFT, name="Hierarchy-Level(1 or 2-3 or 1,3)")
        self.AddEditText(1001, c4d.BFH_SCALEFIT)
        self.SetString(1001, "1")

        self.AddCheckbox(1002, c4d.BFH_LEFT, 0, 0, "add Suffix")

        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
        return True

    def Command(self, id, msg):
        if id == c4d.DLG_OK:
            self.user_input = self.GetString(1001)
            self.add_suffix = self.GetBool(1002)
            self.Close()
            return True
        elif id == c4d.DLG_CANCEL:
            self.user_input = None
            self.Close()
            return False
        return True

def rename_parents(obj, base_name, rename_levels, add_suffix):
    current_level = 1
    parent = obj.GetUp()

    max_level = max(rename_levels) if rename_levels else 0

    while parent and current_level <= max_level:
        if current_level in rename_levels:
            new_name = f"{base_name}_{current_level}" if add_suffix else base_name

            doc.AddUndo(c4d.UNDOTYPE_CHANGE, parent)
            parent.SetName(new_name)

        parent = parent.GetUp()
        current_level += 1

def main():
    dlg = RenameHierarchyDialog()
    if not dlg.Open(c4d.DLG_TYPE_MODAL):
        return

    input_levels = dlg.user_input
    if not input_levels:
        return

    rename_levels = set()
    for part in input_levels.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            rename_levels.update(range(start, end + 1))
        else:
            rename_levels.add(int(part))

    active_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if not active_objects:
        return

    doc.StartUndo()

    for obj in active_objects:
        base_name = obj.GetName()
        rename_parents(obj, base_name, rename_levels, dlg.add_suffix)

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()