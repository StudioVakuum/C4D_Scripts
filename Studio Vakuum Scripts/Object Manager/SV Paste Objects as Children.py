"""
SV Paste Objects as Children
Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.1.0
Description-US: Paste Objects as Children of the selected objects (Keeps original names)
Written for Maxon Cinema 4D 2026.2.0
Python version 3.11.4
"""

import c4d
import re

def get_top_level_guids(doc):
    guids = set()
    op = doc.GetFirstObject()
    while op:
        guids.add(op.GetGUID())
        op = op.GetNext()
    return guids

def main():
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    if not selected_objects:
        c4d.gui.MessageDialog("Please select one or more objects to paste under.")
        return

    all_inserted = []

    for parent in selected_objects:
        before_guids = get_top_level_guids(doc)

        doc.SetActiveObject(None, c4d.SELECTION_NEW)
        c4d.CallCommand(c4d.IDM_PASTE)

        op = doc.GetFirstObject()
        while op:
            if op.GetGUID() not in before_guids:
                next_op = op.GetNext()
                op.Remove()

                clean_name = re.sub(r'\.\d+$', '', op.GetName())
                op.SetName(clean_name)

                doc.InsertObject(op, parent)
                all_inserted.append(op)
                op = next_op
            else:
                op = op.GetNext()

    doc.FlushUndoBuffer()
    doc.StartUndo()
    for obj in all_inserted:
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, obj)
    doc.EndUndo()

    c4d.EventAdd()

if __name__ == '__main__':
    main()