"""
SV Paste Objects as Parents
Author: Yannick Neuhaus (Studio Vakuum) — adapted
Website: https://www.studio-vakuum.com
Version: 1.1.0
Description-US: Paste Objects as Parents of the selected objects (Keeps original names)
Written for Maxon Cinema 4D 2026.2.0
Python version 3.11.4
"""
import c4d
import re

def iter_hierarchy(roots):
    stack = list(roots)
    while stack:
        op = stack.pop(0)
        yield op
        child = op.GetDown()
        while child:
            stack.append(child)
            child = child.GetNext()

def remap_instance_links(clones, guid_map):
    for obj in iter_hierarchy(clones):
        if obj.GetType() == c4d.Oinstance:
            ref = obj[c4d.INSTANCEOBJECT_LINK]
            if ref and ref.GetGUID() in guid_map:
                obj[c4d.INSTANCEOBJECT_LINK] = guid_map[ref.GetGUID()]

def main():
    doc = c4d.documents.GetActiveDocument()
    targets = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)

    if not targets:
        c4d.gui.MessageDialog("Please select one or more objects.")
        return

    doc.StartUndo()

    before = {op.GetGUID() for op in iter_hierarchy([doc.GetFirstObject()])} if doc.GetFirstObject() else set()
    doc.SetActiveObject(None, c4d.SELECTION_NEW)

    c4d.CallCommand(c4d.IDM_PASTE)

    pasted = [op for op in iter_hierarchy([doc.GetFirstObject()]) if op.GetGUID() not in before and op.GetUp() is None]

    for p in pasted:
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, p)

        clean_name = re.sub(r'\.\d+$', '', p.GetName())
        p.SetName(clean_name)

    for target in targets:
        clones = [p.GetClone(c4d.COPYFLAGS_0) for p in pasted]
        guid_map = {o.GetGUID(): c for o, c in zip(iter_hierarchy(pasted), iter_hierarchy(clones))}
        remap_instance_links(clones, guid_map)

        for clone in clones:
            doc.InsertObject(clone, target.GetUp(), target.GetPred())
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)

        if clones:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, target)
            target.Remove()
            target.InsertUnderLast(clones[0])

    for p in pasted:
        doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, p)
        p.Remove()

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == "__main__":
    main()