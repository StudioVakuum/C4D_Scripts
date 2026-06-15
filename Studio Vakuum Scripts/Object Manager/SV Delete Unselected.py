"""
SV Delete Unselected

Author: Yannick Neuhaus (Studio Vakuum)
Website: https://www.studio-vakuum.com
Version: 1.0.0
Description-US: Deletes all objects except the current selection and any objects referenced by selected instances.

Written for Maxon Cinema 4D 2026.3.0 or later
Python version 3.11.4
"""

import c4d

def get_all_objects(op, obj_list):
    while op:
        obj_list.append(op)
        get_all_objects(op.GetDown(), obj_list)
        op = op.GetNext()

def main():
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)

    if not selected_objects:
        return

    doc.StartUndo()

    protected = set()

    for obj in selected_objects:
        if obj.CheckType(c4d.Oinstance):
            protected.add(obj)

            link = obj[c4d.INSTANCEOBJECT_LINK]
            if link:
                protected.add(link)
                children = []
                get_all_objects(link.GetDown(), children)
                protected.update(children)

                parent = link.GetUp()
                while parent:
                    protected.add(parent)
                    parent = parent.GetUp()
        else:
            protected.add(obj)
            children = []
            get_all_objects(obj.GetDown(), children)
            protected.update(children)

    all_objects = []
    get_all_objects(doc.GetFirstObject(), all_objects)

    for obj in reversed(all_objects):
        if obj not in protected:
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
            obj.Remove()

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()