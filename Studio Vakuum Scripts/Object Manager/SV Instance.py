"""
SV Instance

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US:DEFAULT: Creates an instance object for each selected item.<br>SHIFT: Creates a clean duplicate hierarchy of structural Nulls.

Written for Maxon Cinema 4D 2026.2.0 or later
Python version 3.11.4
"""

import c4d
from c4d import gui

def get_top_level_selected(objects):
    obj_set = set(objects)
    top_level = []
    for obj in objects:
        parent = obj.GetUp()
        is_child_of_selection = False
        while parent:
            if parent in obj_set:
                is_child_of_selection = True
                break
            parent = parent.GetUp()
        if not is_child_of_selection:
            top_level.append(obj)
    return top_level, obj_set

def is_referenced_internally(obj, doc, selection_set):
    current = doc.GetFirstObject()
    while current:
        if current.GetType() == c4d.Oinstance:
            if current[c4d.INSTANCEOBJECT_LINK] == obj:
                is_inside_selection = False
                check_parent = current
                while check_parent:
                    if check_parent in selection_set:
                        is_inside_selection = True
                        break
                    check_parent = check_parent.GetUp()

                if is_inside_selection:
                    return True

        if current.GetDown():
            current = current.GetDown()
        elif current.GetNext():
            current = current.GetNext()
        else:
            while current.GetUp() and not current.GetUp().GetNext():
                current = current.GetUp()
            if current.GetUp():
                current = current.GetUp().GetNext()
            else:
                current = None
    return False

def create_instance_hierarchy(obj, doc, selection_set):
    if obj.GetType() == c4d.Onull and is_referenced_internally(obj, doc, selection_set):
        instance_obj = c4d.BaseObject(c4d.Oinstance)
        if not instance_obj:
            return None
        instance_obj.SetName(obj.GetName())
        instance_obj[c4d.INSTANCEOBJECT_LINK] = obj
        instance_obj.SetMl(obj.GetMl())
        return instance_obj

    elif obj.GetType() == c4d.Onull:
        new_null = c4d.BaseObject(c4d.Onull)
        if not new_null:
            return None
        new_null.SetName(obj.GetName())
        new_null.SetMl(obj.GetMl())

        child = obj.GetDown()
        while child:
            new_child = create_instance_hierarchy(child, doc, selection_set)
            if new_child:
                new_child.InsertUnderLast(new_null)
            child = child.GetNext()
        return new_null
    else:
        instance_obj = c4d.BaseObject(c4d.Oinstance)
        if not instance_obj:
            return None
        instance_obj.SetName(obj.GetName())

        target_obj = obj
        if obj.GetType() == c4d.Oinstance:
            nested_target = obj[c4d.INSTANCEOBJECT_LINK]
            if nested_target:
                target_obj = nested_target

        instance_obj[c4d.INSTANCEOBJECT_LINK] = target_obj
        instance_obj.SetMl(obj.GetMl())
        return instance_obj

def main():
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)
    if not selected_objects:
        gui.MessageDialog("Please select at least one object to instance.")
        return

    bc = c4d.BaseContainer()
    gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_QUALIFIER, bc)
    shift_pressed = bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QUALIFIER_SHIFT

    doc.StartUndo()

    new_selection = []

    if shift_pressed:
        top_selected, selection_set = get_top_level_selected(selected_objects)

        for obj in top_selected:
            new_root = create_instance_hierarchy(obj, doc, selection_set)
            if not new_root:
                continue

            doc.InsertObject(new_root, pred=obj.GetPred(), parent=obj.GetUp())
            new_root.SetMg(obj.GetMg())
            new_selection.append(new_root)

            def register_undo_recursive(node):
                doc.AddUndo(c4d.UNDOTYPE_NEW, node)
                child = node.GetDown()
                while child:
                    register_undo_recursive(child)
                    child = child.GetNext()

            register_undo_recursive(new_root)
    else:
        for obj in selected_objects:
            instance_obj = c4d.BaseObject(c4d.Oinstance)
            if not instance_obj:
                continue

            instance_obj.SetName(f"{obj.GetName()}")

            target_obj = obj
            if obj.GetType() == c4d.Oinstance:
                nested_target = obj[c4d.INSTANCEOBJECT_LINK]
                if nested_target:
                    target_obj = nested_target

            instance_obj[c4d.INSTANCEOBJECT_LINK] = target_obj

            doc.InsertObject(instance_obj, pred=obj.GetPred(), parent=obj.GetUp())
            instance_obj.SetMg(obj.GetMg())
            new_selection.append(instance_obj)

            doc.AddUndo(c4d.UNDOTYPE_NEW, instance_obj)

    if new_selection:
        doc.SetActiveObject(None, c4d.SELECTION_NEW)
        for new_obj in new_selection:
            doc.SetActiveObject(new_obj, c4d.SELECTION_ADD)

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
