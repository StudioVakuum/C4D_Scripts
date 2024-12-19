"""
SV Paste Objects as Children

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Paste Objects as Children of the selected objects

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    if not selected_objects:
        c4d.gui.MessageDialog("Please select one or more objects to paste under.")
        return

    null_obj = c4d.BaseObject(c4d.Onull)
    null_obj.SetName("Paste Container")
    doc.InsertObject(null_obj)
    doc.SetActiveObject(null_obj)
    c4d.EventAdd()

    c4d.CallCommand(c4d.IDM_PASTE)
    c4d.EventAdd()

    clipboard_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    if not clipboard_objects:
        return

    doc.StartUndo()

    for parent in selected_objects:
        for obj in reversed(clipboard_objects):
            copy_obj = obj.GetClone()
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, copy_obj)
            copy_obj.InsertUnder(parent)

    for obj in clipboard_objects:
        obj.Remove()

    null_obj.Remove()

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
