"""
SV Paste Objects as Parent

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Paste Objects as Parent of the selected objects

Written for Maxon Cinema 4D 2024.5.1
Python version 3.11.4
"""

import c4d

def find_deepest_child(obj):
    if not obj.GetDown():
        return obj
    
    current_child = obj.GetDown()
    deepest = current_child
    
    while current_child:
        deep_child = find_deepest_child(current_child)
        if deep_child:
            deepest = deep_child
        current_child = current_child.GetNext()
    
    return deepest

def main():
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    
    if not selected_objects:
        c4d.gui.MessageDialog("Please select one or more objects to set as children.")
        return

    null_obj = c4d.BaseObject(c4d.Onull)
    null_obj.SetName("Paste Container")
    doc.InsertObject(null_obj)
    doc.SetActiveObject(null_obj)
    
    c4d.CallCommand(c4d.IDM_PASTE)
    c4d.EventAdd()
    
    pasted_objects = null_obj.GetChildren()
    if not pasted_objects:
        null_obj.Remove()
        return

    doc.StartUndo()
    
    for child in selected_objects:
        for obj in pasted_objects:
            clone = obj.GetClone()
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)
            
            deepest_child = find_deepest_child(clone)
            
            clone.InsertBefore(child)
            
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
            child.InsertUnder(deepest_child)
    
    null_obj.Remove()
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()