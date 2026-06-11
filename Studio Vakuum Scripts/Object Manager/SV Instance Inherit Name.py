"""
SV Instance Inherit Name

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Renames selected Instance objects to match the name of their linked Reference object.

Written for Maxon Cinema 4D 2026.2.0 or later
Python version 3.11.4
"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc:
        return

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not selection:
        c4d.gui.MessageDialog("No objects selected.")
        return

    renamed = 0
    skipped = 0

    doc.StartUndo()

    for obj in selection:
        if obj.GetType() != c4d.Oinstance:
            skipped += 1
            continue

        ref = obj[c4d.INSTANCEOBJECT_LINK]
        if not ref:
            skipped += 1
            continue

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.SetName(ref.GetName())
        renamed += 1

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == "__main__":
    main()